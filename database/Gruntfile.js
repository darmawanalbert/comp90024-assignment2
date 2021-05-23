/*
COMP90024 Team 1
Albert Darmawan (1168452) - darmawana@student.unimelb.edu.au
Clarisca Lawrencia (1152594) - clawrencia@student.unimelb.edu.au
I Gede Wibawa Cakramurti (1047538) - icakramurti@student.unimelb.edu.au
Nuvi Anggaresti (830683) - nanggaresti@student.unimelb.edu.au
Wildan Anugrah Putra (1191132) - wildananugra@student.unimelb.edu.au
*/

module.exports = function (grunt) {
    grunt
      .initConfig({
        "couch-compile": {
          dbs: {
            files: {
              "/tmp/comp90024_tweet_harvest.json": "couchdb/comp90024_tweet_harvest/topic_modelling",
              "/tmp/comp90024_tweet_harvest_summary.json": "couchdb/comp90024_tweet_harvest/summary",
              "/tmp/comp90024_tweet_search.json": "couchdb/comp90024_tweet_search/topic_modelling",
              "/tmp/comp90024_lda_scoring.json": "couchdb/comp90024_lda_scoring/lda_topic"
            }
          }
        },
        "couch-push": {
          options: {
            user: process.env.user,
            pass: process.env.pass
          },
          twitter: {
            files: {
              "http://admin:admin@localhost:15984/comp90024_tweet_harvest": "/tmp/comp90024_tweet_harvest.json",
              "http://admin:admin@localhost:15984/comp90024_tweet_harvest": "/tmp/comp90024_tweet_harvest_summary.json",
              "http://admin:admin@localhost:15984/comp90024_tweet_search": "/tmp/comp90024_tweet_search.json",
              "http://admin:admin@localhost:15984/comp90024_lda_scoring": "/tmp/comp90024_lda_scoring.json"
            }
          }
        }
      });
  
    grunt.loadNpmTasks("grunt-couch");
  };