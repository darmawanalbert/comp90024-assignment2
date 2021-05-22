function (doc) {
    var d = new Date(doc.created_at);
    var date = d.getDate();
    var month = d.getMonth() + 1;
    var year = d.getFullYear();
    if (doc.truncated === true)
      emit([[year, month, date], doc.place.name], 1);
    else
      emit([[year, month, date], doc.place.name], 1);
  }