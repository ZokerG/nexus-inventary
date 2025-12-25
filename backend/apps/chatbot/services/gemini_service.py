import os
from datetime import datetime, timedelta
from google import genai
from google.genai import types
from django.conf import settings


class GeminiService:
    """Servicio para interactuar con Gemini AI"""
    
    def __init__(self):
        # Inicializar cliente de Gemini
        api_key = os.getenv('GEMINI_API_KEY', settings.GEMINI_API_KEY)
        self.client = genai.Client(api_key=api_key)
        self.model_name = "gemini-2.0-flash-exp"
    
    def get_system_instruction(self, user):
        """Genera system instruction personalizado según el usuario"""
        permissions = "crear, editar, eliminar empresas, productos e inventario" if user.is_admin else "consultar empresas e inventario"
        
        return f"""Eres NEXUS AI Assistant, un asistente experto en gestión de inventario.

IMPORTANTE: Tienes acceso a funciones que DEBES USAR para realizar operaciones. NO simules respuestas.

INFORMACIÓN DEL USUARIO ACTUAL:
- Nombre: {user.username}
- Email: {user.email}
- Rol: {user.get_role_display()}
- Permisos: {permissions}

REGLAS CRÍTICAS:
1. SIEMPRE usa las funciones disponibles para realizar operaciones (crear, listar, actualizar, eliminar)
2. NO inventes ni simules respuestas - LLAMA a las funciones reales
3. Cuando el usuario pida crear/actualizar/eliminar/consultar, DEBES llamar a la función correspondiente
4. El parámetro user_email siempre debe ser: {user.email}
5. Después de llamar una función, interpreta su resultado y preséntalo de forma amigable

EJEMPLOS DE USO CORRECTO:
Usuario: "Crea una empresa llamada TechCorp con NIT 900123456"
→ DEBES llamar: create_empresa(nit="900123456", nombre="TechCorp", direccion="...", telefono="...", user_email="{user.email}")

Usuario: "Lista las empresas"
→ DEBES llamar: list_empresas(user_email="{user.email}")

Usuario: "¿Cuántas empresas hay?"
→ DEBES llamar: list_empresas(user_email="{user.email}") y luego contar

FORMATO DE RESPUESTAS:
- Usa emojis: ✅ éxito, ❌ error, 🔒 sin permisos, 📊 datos
- Sé conciso pero amigable
- Siempre basa tu respuesta en el resultado real de las funciones
"""
    
    def create_cache(self, user, tools):
        """Crea un cache de contexto para el usuario"""
        system_instruction = self.get_system_instruction(user)
        
        try:
            cache = self.client.caches.create(
                model=self.model_name,
                config=types.CreateCachedContentConfig(
                    display_name=f"nexus_user_{user.id}",
                    system_instruction=system_instruction,
                    contents=[],
                    ttl="3600s",  # 1 hora
                )
            )
            return cache
        except Exception as e:
            print(f"Error creating cache: {e}")
            return None
    
    def get_or_create_cache(self, session, user, tools):
        """Obtiene cache existente o crea uno nuevo"""
        now = datetime.now()
        
        # Si hay cache y no ha expirado, reutilizarlo
        if session.gemini_cache_name and session.cache_expires_at:
            if session.cache_expires_at > now:
                try:
                    cache = self.client.caches.get(name=session.gemini_cache_name)
                    return cache
                except Exception as e:
                    print(f"Cache not found or expired: {e}")
        
        # Crear nuevo cache
        cache = self.create_cache(user, tools)
        
        if cache:
            # Guardar en sesión
            session.gemini_cache_name = cache.name
            session.cache_expires_at = now + timedelta(hours=1)
            session.save()
        
        return cache
    
    def send_message(self, session, user, message, tools):
        """Envía un mensaje y obtiene respuesta de Gemini con automatic function calling"""
        print(f"\n{'='*80}")
        print(f"🚀 INICIO - send_message")
        print(f"Usuario: {user.email}")
        print(f"Mensaje: {message[:100]}...")
        print(f"Número de tools disponibles: {len(tools)}")
        print(f"{'='*80}\n")
        
        system_instruction = self.get_system_instruction(user)
        
        # Obtener historial de la sesión
        from ..models import ChatMessage
        from ..tools.registry import get_function_map
        
        history = []
        messages = ChatMessage.objects.filter(session=session).order_by('created_at')
        
        print(f"📜 Cargando historial: {messages.count()} mensajes previos")
        
        for msg in messages:
            if msg.role == 'user':
                history.append(types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=msg.content)]
                ))
            elif msg.role == 'model':
                history.append(types.Content(
                    role="model",
                    parts=[types.Part.from_text(text=msg.content)]
                ))
        
        # Agregar el nuevo mensaje del usuario
        history.append(types.Content(
            role="user",
            parts=[types.Part.from_text(text=message)]
        ))
        
        print(f"📝 Historial completo: {len(history)} elementos\n")
        
        try:
            # Configuración de generación con automatic function calling
            config = types.GenerateContentConfig(
                system_instruction=system_instruction,
                tools=[types.Tool(function_declarations=tools)],
                tool_config=types.ToolConfig(
                    function_calling_config=types.FunctionCallingConfig(
                        mode="ANY"  # Forzar que use funciones cuando sea relevante
                    )
                ),
                temperature=0.2,
            )
            
            print(f"🤖 Llamando a Gemini (modelo: {self.model_name})...")
            
            # Primera llamada: Gemini puede decidir llamar funciones
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=history,
                config=config
            )
            
            print(f"✅ Respuesta recibida de Gemini\n")
            
            # Verificar si hay function calls
            function_map = get_function_map()
            tool_calls = []
            has_function_calls = False
            
            # Procesar la respuesta y ejecutar function calls si existen
            if hasattr(response, 'candidates') and response.candidates:
                print(f"🔍 Analizando respuesta: {len(response.candidates)} candidatos")
                
                for candidate in response.candidates:
                    if hasattr(candidate, 'content') and candidate.content.parts:
                        print(f"   - Partes en contenido: {len(candidate.content.parts)}")
                        
                        for part in candidate.content.parts:
                            # Si hay function call, ejecutarlo
                            if hasattr(part, 'function_call') and part.function_call:
                                has_function_calls = True
                                func_name = part.function_call.name
                                func_args = dict(part.function_call.args) if part.function_call.args else {}
                                
                                print(f"\n🔧 FUNCTION CALL DETECTADO:")
                                print(f"   Función: {func_name}")
                                print(f"   Argumentos: {func_args}")
                                
                                tool_calls.append({
                                    'name': func_name,
                                    'args': func_args
                                })
                                
                                # Ejecutar la función
                                if func_name in function_map:
                                    print(f"   ⚙️  Ejecutando función {func_name}...")
                                    func_result = function_map[func_name](**func_args)
                                    print(f"   ✅ Resultado: {func_result}\n")
                                    
                                    # Agregar el function call al historial
                                    history.append(types.Content(
                                        role="model",
                                        parts=[types.Part.from_function_call(
                                            name=func_name,
                                            args=func_args
                                        )]
                                    ))
                                    
                                    # Agregar el resultado de la función al historial
                                    history.append(types.Content(
                                        role="user",  # El resultado viene como "user"
                                        parts=[types.Part.from_function_response(
                                            name=func_name,
                                            response=func_result
                                        )]
                                    ))
                                else:
                                    print(f"   ❌ ERROR: Función {func_name} no encontrada en function_map")
                            elif hasattr(part, 'text') and part.text:
                                print(f"   📄 Texto directo: {part.text[:100]}...")
            
            # Si hubo function calls, hacer una segunda llamada para obtener la respuesta final
            if has_function_calls:
                print(f"\n🔄 Enviando resultados de funciones a Gemini para respuesta final...")
                
                # Config sin forzar function calling para la respuesta final
                final_config = types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    tools=[types.Tool(function_declarations=tools)],
                    tool_config=types.ToolConfig(
                        function_calling_config=types.FunctionCallingConfig(
                            mode="NONE"  # No permitir más function calls, solo respuesta
                        )
                    ),
                    temperature=0.2,
                )
                
                final_response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=history,
                    config=final_config
                )
                
                final_text = ""
                if hasattr(final_response, 'candidates') and final_response.candidates:
                    for candidate in final_response.candidates:
                        if hasattr(candidate, 'content') and candidate.content.parts:
                            for part in candidate.content.parts:
                                if hasattr(part, 'text') and part.text:
                                    final_text += part.text
                
                # Si no hay texto en la respuesta final, usar el mensaje de la función
                if not final_text:
                    print(f"⚠️  Gemini no generó texto final, usando resultados de funciones")
                    for call in tool_calls:
                        # Buscar el resultado en el historial
                        for content in history:
                            if content.role == "user" and hasattr(content.parts[0], 'function_response'):
                                func_resp = content.parts[0].function_response
                                if func_resp.name == call['name']:
                                    result = func_resp.response
                                    if isinstance(result, dict) and 'message' in result:
                                        final_text += result['message'] + "\n"
                
                print(f"✅ Respuesta final recibida")
                print(f"📨 Texto final: {final_text[:200] if final_text else 'Sin texto'}...\n")
                
                return {
                    'text': final_text if final_text else "✅ Operación completada",
                    'tool_calls': tool_calls,
                    'usage': final_response.usage_metadata if hasattr(final_response, 'usage_metadata') else None
                }
            else:
                # No hubo function calls, retornar la respuesta directa
                print(f"ℹ️  No se detectaron function calls")
                print(f"📨 Respuesta directa: {response.text[:200] if response.text else 'Sin texto'}...\n")
                
                return {
                    'text': response.text if response.text else "✅ Operación completada",
                    'tool_calls': None,
                    'usage': response.usage_metadata if hasattr(response, 'usage_metadata') else None
                }
        
        except Exception as e:
            import traceback
            print(f"\n❌ ERROR EN send_message:")
            print(f"   Tipo: {type(e).__name__}")
            print(f"   Mensaje: {str(e)}")
            print(f"   Traceback:")
            traceback.print_exc()
            print(f"{'='*80}\n")
            
            return {
                'text': f"❌ Error al procesar tu mensaje: {str(e)}",
                'tool_calls': None,
                'error': str(e)
            }
    
    def send_message_stream(self, session, user, message, tools):
        """Envía mensaje con streaming (para respuestas en tiempo real)"""
        system_instruction = self.get_system_instruction(user)
        
        # Obtener historial de la sesión
        from ..models import ChatMessage
        history = []
        messages = ChatMessage.objects.filter(session=session).order_by('created_at')
        
        for msg in messages:
            if msg.role == 'user':
                history.append(types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=msg.content)]
                ))
            elif msg.role == 'model':
                history.append(types.Content(
                    role="model",
                    parts=[types.Part.from_text(text=msg.content)]
                ))
        
        # Agregar el nuevo mensaje
        history.append(types.Content(
            role="user",
            parts=[types.Part.from_text(text=message)]
        ))
        
        try:
            config = types.GenerateContentConfig(
                system_instruction=system_instruction,
                tools=tools,
                temperature=0.2,
            )
            
            response = self.client.models.generate_content_stream(
                model=self.model_name,
                contents=history,
                config=config
            )
            
            for chunk in response:
                if chunk.text:
                    yield chunk.text
        
        except Exception as e:
            yield f"❌ Error: {str(e)}"
