const { encrypt, decrypt } = require('./encryption');

const message = 'Hello, world!';
const encryptedMessage = encrypt(message);
const decryptedMessage = decrypt(encryptedMessage);

console.log('Original message:', message);
console.log('Encrypted message:', encryptedMessage);
console.log('Decrypted message:', decryptedMessage);
