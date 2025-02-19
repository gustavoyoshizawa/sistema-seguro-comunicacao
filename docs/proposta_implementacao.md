# Proposta de Implementação:

## bcrypt
bcrypt protege as senhas armazenadas ao aplicar um sal aleatório e múltiplas iterações de hashing. Isso impede que senhas sejam armazenadas de forma insegura e dificulta ataques de força bruta ou rainbow tables.

## PyJWT
PyJWT permite autenticar usuários criando tokens JWT assinados. Esses tokens contêm informações do usuário e têm um tempo de expiração, garantindo que apenas usuários autenticados possam acessar áreas protegidas.

## AES (Advanced Encryption Standard)
AES usa uma chave simétrica para criptografar e descriptografar mensagens de forma rápida e segura. No modo CBC, um vetor de inicialização aleatório é usado, garantindo que cada mensagem seja única e protegida contra ataques.

## RSA (Rivest-Shamir-Adleman)
RSA criptografa a chave AES com a chave pública do destinatário. Apenas o destinatário pode usar sua chave privada para descriptografá-la, garantindo que a chave de criptografia da mensagem fique segura.

Principais etapas de implementação, incluindo:
✅ Cadastro de usuário → Hash de senha com bcrypt.
✅ Login → Geração e verificação de Token JWT.
✅ Criptografia de mensagens → Uso de AES (CBC).
✅ Proteção da chave AES → Uso de RSA para criptografar a chave antes de armazená-la.
Breve explicação sobre armazenamento seguro de dados.
