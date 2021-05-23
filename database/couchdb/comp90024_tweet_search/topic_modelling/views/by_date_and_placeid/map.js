function (doc) {
  var d = new Date(doc.created_at);
  var date = d.getDate();
  var month = d.getMonth() + 1;
  var year = d.getFullYear();
  emit([[year, month, date], doc.AURIN_id], {id: doc._id, text: doc.text, aurin_loc: doc.AURIN_loc_name.toLowerCase(), coordinates: doc.coordinates});
}