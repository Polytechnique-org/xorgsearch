import template from './template.html'

export default {
  name: 'SearchResults',
  template: template,
  props: ['msgbus'],
  data: function () {
    return {
      profiles: [],
    }
  },
  created: function () {
    this.msgbus.$on('search-result', function(results) {
      this.profiles = results.profiles
    }.bind(this))
  }
}
