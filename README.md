# Q&A Review Application

A Streamlit web application for reviewing **PhD Viva** questions and answers with an integrated glossary of terms. Supports section filtering, random question selection, and mobile-friendly responsive design.

## Features
- Interactive Q&A navigation with progress tracking
- Section-based filtering system
- Glossary with custom-styled HTML table
- Responsive design for desktop and mobile
- Tabbed interface for Q&A and glossary

## Requirements
- Python 3.8+ (developed on 3.13)
- Streamlit, pandas, Pillow

## File Structure
- `data/viva.csv`: Q&A data with columns: Section, Question Number, Question, Answer
- `data/glossary.csv`: Glossary with columns: Term, Definition
- `images/logo.png`: Application logo

## Deployment
Ready for Streamlit Community Cloud deployment

## License
This project is provided for educational purposes. Feel free to use and modify.

## Notes
The order of streamlit processing is top-down, so the filtering has been placed
at the top of the UI for simplicity's sake.  An exercise for the willing, would be to put this at the bottom of the UI where it arguably belongs, as it is not the app's primary focus.  

I prefer it where it is, as I tend to review only one section at a time, so I 
constantly change them.  For general use, this belongs rightfully at the bottom
of the page.    

You will impose some wiring, event, and state-management peculiarities upon yourself, but you may find it worthwhile.  