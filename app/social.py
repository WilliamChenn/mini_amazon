from flask import Blueprint, render_template
from flask_login import current_user

from app.models.reviews import Reviews


bp = Blueprint('social', __name__)

@bp.route('/recent-reviews', methods=['GET'])
def recent_reviews():
    
    if current_user.is_authenticated:
        reviews = Reviews.get_by_user_id(current_user.id)
    else:
        reviews = None
    
    return render_template('reviews.html', reviews=reviews)