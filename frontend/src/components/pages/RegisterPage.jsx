import React from 'react';
import AuthTemplate from '../templates/AuthTemplate';
import RegisterForm from '../organisms/RegisterForm';

const RegisterPage = () => {
  return (
    <AuthTemplate>
      <RegisterForm />
    </AuthTemplate>
  );
};

export default RegisterPage;
