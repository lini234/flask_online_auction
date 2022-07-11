from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import listings
from sqlalchemy import or_

# Create main blueprint
mainbp = Blueprint('main', __name__)

@mainbp.route('/')
def index():
    listing = listings.query.filter_by(status='Active').all()
    return render_template('index.html', listing=listing)

@mainbp.route('/search')
def search():
    #get the search string from request
    if request.args['search']:
        item = "%" + request.args['search'] + '%'
    #use filter and like function to search for matching item
        listing = listings.query.filter(
            or_(
                listings.title.like(item),
                listings.cpu.like(item),
                listings.brand.like(item),
                listings.ram_gb.like(item),
                listings.storage_gb.like(item)
            ), listings.status == 'Active'
        )
        # Search result message
        resultMessage = "{0} results matching '{1}'".format(listing.count(), request.args['search'])
        flash (resultMessage)
        return render_template('index.html', listings=listing)
    else:
        return redirect(url_for('main.index'))