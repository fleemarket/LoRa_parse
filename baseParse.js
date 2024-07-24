const base64ToHex = (str) => {
    const raw = atob(str);
    let result = "";
    for (let i = 0; i < raw.length; i++) {
        const hex = raw.charCodeAt(i).toString(16);
        result += hex.length === 2 ? hex : "0" + hex;
    }
    return result.toUpperCase();
};

const parse = (str) => {
    const average = parseInt(str.slice(2, 6), 16);
    const imageData = str.slice(6);
    const image = [];
    for (let i = 0; i < imageData.length / 2; i++) {
        pie = parseInt(imageData.slice(i * 2, i * 2 + 2), 16);
        if ((pie & 0x80) > 0) {
            pie = pie - 0x100;
        }

        image.push(average + pie);
    }
    return image;
};

let none = [];

none = parse(
    base64ToHex(
        "BgDyAfr/AQH+Av8EAQMDAwIFBAQEBQIDAQQBAQAA/wD8APr6/wD//gABBQIFAQMCAwMH"
    )
);
console.log(none);
