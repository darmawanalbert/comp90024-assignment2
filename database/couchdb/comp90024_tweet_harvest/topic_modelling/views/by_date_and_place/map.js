function (doc) {
  var d = new Date(doc.created_at);
  var date = d.getDate();
  var month = d.getMonth() + 1;
  var year = d.getFullYear();
  
  city_dict = {'Australian Capital Territory': 'Canberra - Queanbeyan (Canberra Part)', 'Western Australia': 'Perth (WA)',
  'Blue Mountains National Park': 'Blue Mountains', 'New South Wales' : 'Sydney', 'Victoria': 'Melbourne', 'South Australia': 'Adelaide',
  'Northern Territory': 'Darwin', 'Tasmania': 'Hobart', 'Queensland': 'Brisbane', 'Canberra': 'Canberra - Queanbeyan (Canberra Part)'
  }
  if (doc.place.name in city_dict)
    place_name = city_dict[doc.place.name];
  else
    place_name = doc.place.name
  
  if (doc.truncated === true && doc.AURIN_loc_name)
    emit([[year, month, date], doc.AURIN_loc_name.toLowerCase()], {id: doc._id, text: doc.extended_tweet.full_text, aurin_id: doc.AURIN_id, coordinates: doc.coordinates});
  else if (doc.truncated === false && doc.AURIN_loc_name)
    emit([[year, month, date], doc.AURIN_loc_name.toLowerCase()], {id: doc._id, text: doc.text, aurin_id: doc.AURIN_id, coordinates: doc.coordinates});
  else if (doc.truncated === true)
    emit([[year, month, date], place_name.toLowerCase()], {id: doc._id, text: doc.extended_tweet.full_text, coordinates: doc.coordinates});
  else
    emit([[year, month, date], place_name.toLowerCase()], {id: doc._id, text: doc.text, coordinates: doc.coordinates});
}