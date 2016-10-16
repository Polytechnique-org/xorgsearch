/*
 * Imports section.
 * Order them as follows:
 *
 * - External libraries (jQuery, Leaflet, Fetch, ...)
 * - Business-owned libraries, if any;
 * - Internal imports from within the app.
 */

import Vue from 'vue'

import SearchPage from 'src/components/searchpage'

/* eslint-disable no-new */
new Vue({
  el: '#xorgsearch',
  components: {
    'search-page': SearchPage
  },
})
