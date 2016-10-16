
const payload = {
  profiles: [
    {
      'hrpid': 'louis.vaneau.1829',
    }
  ]
}


class SearchEngine {
  constructor(endPoint, bus) {
    this.endPoint = endPoint
    this.currentQuery = null
    this.bus = bus

    this.setupHandlers()
  }

  onSearchTrigger(query) {
    if (this.currentQuery == query) {
      // Same query: ignore
      return
    }

    this.currentQuery = query
    new Promise(function(resolve, reject) {
      window.setTimeout(resolve, 2000)
    }).then(this.onSearchResult.bind(this))

    // Notify UIs we're searching
    this.bus.$emit('search-status', 'loading')
  }

  onSearchResult() {
    this.bus.$emit('search-status', 'loaded')
    this.bus.$emit('search-result', payload)
  }

  setupHandlers() {
    this.bus.$on('search-trigger', this.onSearchTrigger.bind(this))
  }
}


function setupSearchEngine(endPoint, msgBus) {
  console.log("Setting up search engine: endpoint=" + endPoint + "; bus=" + msgBus)
  var engine = new SearchEngine(endPoint, msgBus)
}


export default setupSearchEngine
