var infoBox_ratingType = 'star-rating';

// Infobox Output
function locationData(locationURL,locationImg,locationTitle, locationAddress, locationRating, locationRatingCounter) {
  return(''+
    '<a href="'+ locationURL +'" class="listing-img-container">'+
       '<div class="infoBox-close"><i class="fa fa-times"></i></div>'+
       '<img src="'+locationImg+'" alt="">'+

       '<div class="listing-item-content">'+
          '<h3>'+locationTitle+'</h3>'+
          '<span>'+locationAddress+'</span>'+
       '</div>'+

    '</a>'+

    '<div class="listing-content">'+
       '<div class="listing-title">'+
          '<div class="'+infoBox_ratingType+'" data-rating="'+locationRating+'"><div class="rating-counter">('+locationRatingCounter+' reviews)</div></div>'+
       '</div>'+
    '</div>')
}

// Locations

// icons available
// http://fontawesome.io/icons/ fa fa-flask
// https://iconsmind.com/view_icons/ im im-icon-Gears
// http://simplelineicons.com/ sl sl-icon-user

  var locations = [
    [ locationData('listings-single-page.html','/static/img/listing-item-01.jpg',"Tom's Restaurant",'964 School Street, New York', '3.5', '12'), 40.94401669296697, -74.16938781738281, 1, '<i class="fa fa-flask"></i>'],
    [ locationData('listings-single-page.html','/static/img/listing-item-02.jpg','Sticky Band','Bishop Avenue, New York', '5.0', '23'), 40.77055783505125, -74.26002502441406,          2, '<i class="im im-icon-Data-Center"></i>'],
    [ locationData('listings-single-page.html','/static/img/listing-item-03.jpg','Hotel Govendor','778 Country Street, New York', '2.0', '17'), 40.7427837, -73.11445617675781,         3, '<i class="im im-icon-Gears"></i>' ],
    [ locationData('listings-single-page.html','/static/img/listing-item-04.jpg','Burger House','2726 Shinn Street, New York', '5.0', '31'), 40.70437865245596, -73.98674011230469,     4, '<i class="fa fa-laptop"></i>' ],
    [ locationData('listings-single-page.html','/static/img/listing-item-05.jpg','Airport','1512 Duncan Avenue, New York', '3.5', '46'), 40.641311, -73.778139,                         5, '<i class="im im-icon-DNA-2"></i>'],
    [ locationData('listings-single-page.html','/static/img/listing-item-06.jpg','Think Coffee','215 Terry Lane, New York', '4.5', '15'), 41.080938, -73.535957,                        6, '<i class="im im-icon-Clinic"></i>'], 
  ];