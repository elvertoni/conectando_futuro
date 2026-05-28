import os
import logging
from django.conf import settings
from django.template.loader import render_to_string
from .models import Resume

logger = logging.getLogger(__name__)

try:
    from weasyprint import HTML
    WEASYPRINT_AVAILABLE = True
except Exception as e:
    logger.warning(f"WeasyPrint could not be imported: {str(e)}. Fallback to browser print will be active.")
    WEASYPRINT_AVAILABLE = False

def generate_pdf(resume_id):
    """
    Renders the resume HTML and generates a PDF using WeasyPrint.
    If WeasyPrint is not available or fails, returns False to trigger the browser printing fallback.
    """
    try:
        resume = Resume.objects.prefetch_related('education', 'experience').get(id=resume_id)
    except Resume.DoesNotExist:
        logger.error(f"Resume {resume_id} not found")
        return False

    context = {
        'resume': resume,
        'user': resume.user,
        'education_list': resume.education.all(),
        'experience_list': resume.experience.all(),
    }
    html_content = render_to_string('resume/pdf_template.html', context)
    
    user_dir = os.path.join(settings.MEDIA_ROOT, 'curriculos', str(resume.user.id))
    os.makedirs(user_dir, exist_ok=True)
    
    filename = f'curriculo_v{resume.version}.pdf'
    filepath = os.path.join(user_dir, filename)
    
    if not WEASYPRINT_AVAILABLE:
        logger.warning(f"WeasyPrint is not available. Skipping PDF file generation for resume {resume_id}.")
        return False
        
    try:
        # Generate PDF using WeasyPrint
        HTML(string=html_content).write_pdf(filepath)
        
        # Save filepath to model (relative path)
        relative_path = f"curriculos/{resume.user.id}/{filename}"
        resume.pdf_file = relative_path
        resume.save()
        
        logger.info(f"PDF successfully generated for resume {resume_id} at {filepath}")
        return True
    except Exception as e:
        logger.error(f"WeasyPrint error generating PDF for resume {resume_id}: {str(e)}")
        return False
