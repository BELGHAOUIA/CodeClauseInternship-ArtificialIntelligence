from django.shortcuts import render

from django.core.files.uploadedfile import InMemoryUploadedFile


from textblob import TextBlob

def index(request):
    result = ''
    paragraph_input = ''

    if request.method == 'POST':
        if 'analyze_paragraph' in request.POST:
            paragraph_input = request.POST.get('paragraph_input', '').strip()
            
            if paragraph_input:
                blob = TextBlob(paragraph_input)
                sentiment = blob.sentiment.polarity
                if sentiment < 0:
                    sentiment = "negative"
                elif sentiment == 0:
                    sentiment = "neutral"
                else :
                    sentiment = "positive"
                result = f'Paragraph Analysis: the review is {sentiment}.'
            else:
                result = 'No paragraph entered. Please provide a valid input.'

        elif 'analyze_file' in request.POST:
            file: InMemoryUploadedFile = request.FILES.get('file_input')
            
            if file:
                try:
                    file_content = file.read().decode('utf-8').strip()
                    print(file_content)
                    if file_content:
                         lines = file_content.splitlines()
                         line_results = 0

                         for index, line in enumerate(lines, 1):
                             blob = TextBlob(line)
                             sentiment = blob.sentiment.polarity
                             line_results += sentiment
                         line_results /= index
                         print(line_results)
                         if line_results < 0:
                            line_results = "negative"
                         elif line_results == 0:
                            line_results = "neutral"
                         else :
                            line_results = "positive"
                         result = f'File Analysis: The reviews are mostly {line_results}.'
                    else:
                        result = 'The uploaded file is empty. Please upload a file with content.'
                
                except Exception as e:
                    result = f'Error reading the file: {e}'
            else:
                result = 'No file uploaded. Please upload a valid text file.'

    return render(request, 'index.html', {
        'result': result,
        'paragraph_input': paragraph_input
    })
