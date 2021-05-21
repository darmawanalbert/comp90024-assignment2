function (doc) {
    var d = new Date(doc.created_at);
    var date = d.getDate();
    var month = d.getMonth() + 1;
    var year = d.getFullYear();
    if (doc.truncated === true)
      emit([[year, month, date], doc.place.name], {id: doc._id, text: doc.extended_tweet.full_text, coordinates: doc.coordinates});
    else
      emit([[year, month, date], doc.place.name], {id: doc._id, text: doc.text, coordinates: doc.coordinates});
  }