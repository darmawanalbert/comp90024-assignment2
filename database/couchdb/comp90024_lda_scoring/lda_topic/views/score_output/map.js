function (doc) {
  var d = doc.date // String format such as "2021,5,9"
  d = d.split(",");
  for (i=0; i<d.length; i++) {
    d_i = d[i].trim();
    d_i = parseInt(d_i);
    d[i] = d_i;
  }
  emit([d, doc.location], {lda_keywords: doc.lda_result, topic_score: {sport: doc.score_sports,
      places: doc.score_places, politics: doc.score_politics, education: doc.score_education,
      entertainment: doc.score_entertainment, business: doc.score_business}});
  }