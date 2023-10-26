const enc_flag = "6061284128896791571647435710888326"
// const flag = "UiTHack24{t3st_fl4g}"

const encrypt = input => {
    let encrypted = ""
    for (let idx = 0; idx < input.length; idx++) {
        encrypted += (input.charCodeAt(idx) ^ input.charCodeAt(idx+1 % input.length)).toString(16).padStart(2, "0");
    }
    return encrypted
}

// split enc_flag into pairs of two
const flag_enc = "3c3d1c29020859064f0f4740072b390a58531a7d"
let pairs = flag_enc.match(/.{1,2}/g)
console.log(pairs)
prev = "}"

// Decrypt
var flag = "}"
for(let i = pairs.length-2; i >= 0; i--) {
    flag += String.fromCharCode(parseInt(pairs[i], 16) ^ prev.charCodeAt(0))
    prev = flag[flag.length-1]
}
// print the reverse of flag
console.log(flag.split("").reverse().join(""))