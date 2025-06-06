export const includesCaseInsensitive = (str, searchString) => {
    const normalizeArabic = (s) =>
        s
            .normalize('NFKD')
            .replace(/[\u064B-\u065F\u0670\u06D6-\u06ED]/g, '')
            .replace(/ٱ/g, 'ا')
            .toLowerCase();
    return normalizeArabic(str).includes(normalizeArabic(searchString));
};

export const boldMatchedWord = (str, searchString) => {
    const normalizeArabic = (s) =>
        s
            .normalize('NFKD')
            .replace(/[\u064B-\u065F\u0670\u06D6-\u06ED]/g, '')
            .replace(/ٱ/g, 'ا')
            .toLowerCase();

    const normalizedStr = normalizeArabic(str);
    const normalizedSearch = normalizeArabic(searchString);

    const regex = new RegExp(`(${normalizedSearch})`, 'gi');

    return str.replace(regex, (match) => {
        return `<span class="font-bold underline">${match}</span>`;
    });
};

export const isValidString = (str) => {
    return typeof str?.trim === 'function' && str.trim() !== '';
}

export const isArabic = (str) => {
    const arabicRegex = /[\u0600-\u06FF]/;
    return arabicRegex.test(str);
}

export const toArabicNumber = (num) => {
    const arabicNumbers = ['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩'];
    return num.toString().split('').map(digit => arabicNumbers[digit]).join('');
}

export const getRandomNumberInRange = async (min, max) => {
    const response = await fetch('https://beacon.nist.gov/beacon/2.0/pulse/last');
    const data = await response.json();
    const hexStr = data.pulse.outputValue;
    const bigInt = BigInt('0x' + hexStr);
    const rangeSize = BigInt(max - min + 1);
    const randomInRange = (bigInt % rangeSize) + BigInt(min);
    return Number(randomInRange);
} 