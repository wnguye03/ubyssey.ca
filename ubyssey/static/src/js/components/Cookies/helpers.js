import Cookies from 'js-cookie';

export const getCookie = (name, field) => {
  let cookie = Cookies.get(name)
  if (typeof cookie === 'string' && cookie !== '') {
    cookie = JSON.parse(cookie)
    if (field) {
      return cookie[field]
    }
    return cookie
  }
  return cookie
}

export const setCookie = (name, values) => {
  Cookies.set(
    name,
    values,
    { path: '/' }
  )
}