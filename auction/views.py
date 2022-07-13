from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Listings
from sqlalchemy import or_

# Create main blueprint
mainbp = Blueprint('main', __name__)

@mainbp.route('/')
def index():
    listing = Listings.query.filter_by(status='Active').all()
    return render_template('index.html', listing=listing)

@mainbp.route('/search')
def search():
    #get the search string from request
    if request.args['search']:
        item = "%" + request.args['search'] + '%'
    #use filter and like function to search for matching item
        listing = Listings.query.filter(
            or_(
                Listings.title.like(item),
                Listings.cpu.like(item),
                Listings.brand.like(item),
                Listings.ram_gb.like(item),
                Listings.storage_gb.like(item)
            ), Listings.status == 'Active'
        )
        # Search result message
        resultMessage = "{0} results matching '{1}'".format(listing.count(), request.args['search'])
        flash (resultMessage)
        return render_template('index.html', listings=listing)
    else:
        return redirect(url_for('main.index'))