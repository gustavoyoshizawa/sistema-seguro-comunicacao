# Definição de Funcionalidades

✅ Cadastro de usuário → Protege a senha com bcrypt antes de armazenar.

✅ Login → Se a senha estiver correta, gera um Token JWT.

✅ Enviar mensagem → A mensagem é criptografada com AES antes de ser salva.

✅ Receber mensagem → O usuário descriptografa com RSA sua chave AES e acessa a mensagem.
