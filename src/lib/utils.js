//export const includesCaseInsensitive = (str, searchString) => new RegExp(searchString, 'i').test(str);

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

export const isArabic = (str) => {
    const arabicRegex = /[\u0600-\u06FF]/;
    return arabicRegex.test(str);
}

export const toArabicNumber = (num) => {
    const arabicNumbers = ['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩'];
    return num.toString().split('').map(digit => arabicNumbers[digit]).join('');
}