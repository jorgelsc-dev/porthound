import { register } from 'register-service-worker'

const enableServiceWorker =
  process.env.NODE_ENV === 'production' &&
  process.env.VUE_APP_ENABLE_SERVICE_WORKER === 'true'

function unregisterExistingServiceWorkers () {
  if (typeof window === 'undefined' || !('serviceWorker' in navigator)) return
  window.addEventListener('load', () => {
    navigator.serviceWorker
      .getRegistrations()
      .then((registrations) => {
        registrations.forEach((registration) => registration.unregister())
      })
      .catch((error) => {
        console.error('Error unregistering service workers:', error)
      })
  })
}

if (enableServiceWorker) {
  register(`${process.env.BASE_URL}service-worker.js`, {
    ready () {
      console.log(
        'App is being served from cache by a service worker.\n' +
        'For more details, visit https://goo.gl/AFskqB'
      )
    },
    registered () {
      console.log('Service worker has been registered.')
    },
    cached () {
      console.log('Content has been cached for offline use.')
    },
    updatefound () {
      console.log('New content is downloading.')
    },
    updated () {
      console.log('New content is available; please refresh.')
    },
    offline () {
      console.log('No internet connection found. App is running in offline mode.')
    },
    error (error) {
      console.error('Error during service worker registration:', error)
    }
  })
} else {
  unregisterExistingServiceWorkers()
}
