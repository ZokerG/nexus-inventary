import React from 'react';
import AuthTemplate from '../templates/AuthTemplate';
import LoginForm from '../organisms/LoginForm';

const LoginPage = () => {
  return (
    <AuthTemplate>
      <LoginForm />
    </AuthTemplate>
  );
};

export default LoginPage;
