function writeToFile(path: string, content: any, encoding?: string): boolean {
    encoding = encoding || 'utf-8';
    content = content instanceof String ? content : content.toString();
    const file = new File(path);
    file.encoding = encoding;
    file.open('w');
    const isSuccess: boolean = file.write(content);
    file.close();

    return isSuccess;
}

export { writeToFile };