document.getElementById('extract').addEventListener('click', async () => {
    const fileInput = document.getElementById('file');
    const character = document.getElementById('character').value;
    const resultDiv = document.getElementById('result');
    
    if (fileInput.files.length === 0) {
        alert('Please select a file.');
        return;
    }
    
    const file = fileInput.files[0];
    const reader = new FileReader();
    
    reader.onload = async (e) => {
        const pdfBytes = new Uint8Array(e.target.result);
        const pdfDoc = await PDFLib.PDFDocument.load(pdfBytes);
        const pages = pdfDoc.getPages();
        let text = '';
        
        for (const page of pages) {
            const { textContent } = await page.getTextContent();
            text += textContent.items.map(item => item.str).join(' ');
        }
        
        const pattern = /([A-Z]+:)/g;
        const splitText = text.split(pattern);
        let combinedText = [];
        
        for (let i = 1; i < splitText.length; i += 2) {
            combinedText.push(splitText[i] + splitText[i + 1]);
        }
        
        if (splitText.length && !pattern.test(splitText[0])) {
            combinedText = [splitText[0]].concat(combinedText);
        }
        
        const filteredText = combinedText.filter(item => item.startsWith(character));
        resultDiv.innerHTML = filteredText.map(item => `<p>${item}</p>`).join('');
    };
    
    reader.readAsArrayBuffer(file);
});
