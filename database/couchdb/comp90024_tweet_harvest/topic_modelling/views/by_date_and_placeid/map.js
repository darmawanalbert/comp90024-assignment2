function (doc) {
  var d = new Date(doc.created_at);
  var date_v2 = new Date('2021-05-24')
  if (d > date_v2) {
    var date = d.getDate();
    var month = d.getMonth() + 1;
    var year = d.getFullYear();
    if (doc.truncated === true)
      emit([[year, month, date], doc.AURIN_id], {id: doc._id, text: doc.extended_tweet.full_text, aurin_loc: doc.AURIN_loc_name.toLowerCase(), coordinates: doc.coordinates});
    else
      emit([[year, month, date], doc.AURIN_id], {id: doc._id, text: doc.text, aurin_loc: doc.AURIN_loc_name.toLowerCase(), coordinates: doc.coordinates});
  }
}