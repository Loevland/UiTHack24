const enc_flag = "3c3d1c29020859064f115e4242471011434147686e046a3e0f316b585d540b3133585a09124153544e7d"

const encrypt = input => {
    let encrypted = ""
    for (let idx = 0; idx < input.length; idx++) {
        encrypted += (input.charCodeAt(idx) ^ input.charCodeAt(idx+1 % input.length)).toString(16).padStart(2, "0");
    }
    return encrypted
}

// ask the user for input and check if it matches the encrypted flag
const readline = require('readline');
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

rl.question('What is the password? ', (answer) => {
    if (encrypt(answer) === enc_flag) {
        console.log('Correct!');
    } else {
        console.log('Wrong!');
    }
    rl.close();
});