# Sistema Seguro de Comunicação

Este projeto tem como objetivo criar um sistema seguro de comunicação entre os funcionários de uma empresa. O foco principal é garantir a segurança das credenciais dos usuários e das mensagens armazenadas, utilizando criptografia simétrica (AES), criptografia assimétrica (RSA), hashing de senhas (bcrypt) e autenticação com Tokens JWT.

## Tecnologias Utilizadas
- **bcrypt**: Hashing seguro de senhas.
- **PyJWT**: Autenticação via Tokens JWT.
- **cryptography**: Implementação de AES e RSA.
- **hashlib, base64, os**: Suporte auxiliar.

## Funcionalidades
- Cadastro de usuários com proteção de senha.
- Login com autenticação via JWT.
- Criptografia e descriptografia de mensagens.
