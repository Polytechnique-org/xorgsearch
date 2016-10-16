import Spinner from 'src/components/spinner'

import template from './template.html'

export default {
  name: 'SearchBar',
  template: template,
  props: ['msgbus'],
  data: function() {
    return {
      userQuery: '',
      loading: false,
    }
  },
  computed: {
    parsedQuery: function () {
      return '<<' + this.userQuery + '>>'
    },
  },
  created: function () {
    this.msgbus.$on('search-status', function(searchStatus) {
      this.loading = (searchStatus == 'loading')
    }.bind(this))
  },
  methods: {
    onSubmit: function (event) {
      this.msgbus.$emit('search-trigger', this.parsedQuery)
    },
  },
  components: {
    'spinner': Spinner,
  },
}
