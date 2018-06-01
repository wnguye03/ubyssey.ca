import fetch from 'isomorphic-fetch'
import url from 'url'

const API_URL = '/api/'

const DEFAULT_HEADERS = {
  'Content-Type': 'application/json'
}

function buildRoute(route, id) {
  let pieces = route.split('.')

  let fullRoute = API_URL + pieces[0]
  if (id) {
    fullRoute += `/${id}/`
  }
  if (pieces.length > 1) {
    fullRoute += pieces[1]
  }
  // Append slash to all urls
  let lastCharacter = fullRoute.slice(-1)

  if (lastCharacter !== '/') {
    fullRoute += '/'
  }
  return fullRoute
}

function handleError(response) {
  return response.ok ? response : Promise.reject(response.statusText)
}

function parseJSON(response) {
  return response.json()
    .then(json => response.ok ? json : Promise.reject(json))
}

function getRequest(route, id=null, query={}) {
  let urlString = buildRoute(route, id) + url.format({ query: query })
  return fetch(
    urlString,
    {
      method: 'GET',
      headers: DEFAULT_HEADERS
    }
  )
  .then(parseJSON)
}

function postRequest(route, id=null, payload={}) {
  return fetch(
    buildRoute(route, id),
    {
      // credentials: 'include',
      method: 'POST',
      headers: DEFAULT_HEADERS,
      body: JSON.stringify(payload),
    }
  )
  .then(parseJSON)
}

const DispatchAPI = {
  polls: {
    vote: (payload) => {
      return postRequest('vote', null, payload)
    },
    getResults: (id) => {
      return getRequest('polls', id, null)
    }
  }
}

export default DispatchAPI