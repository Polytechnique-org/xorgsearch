import SearchBar from 'src/components/searchbar'
import SearchResults from 'src/components/searchresults'
import msgBus from 'src/msgbus'
import setupSearchEngine from 'src/services/search'

import template from './template.html'

export default {
  name: 'SearchPage',
  data: function() {
    return {
      'msgbus': msgBus,
    }
  },
  created: function () {
    console.log('SearchPage created: this=' + this + '; msgbus=' + this.msgbus)
    setupSearchEngine('', this.msgbus)
  },
  template: template,
  components: {
    'search-bar': SearchBar,
    'search-results': SearchResults,
  },
}
