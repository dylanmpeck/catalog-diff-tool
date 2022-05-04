/**
 * Copyright 2021 Google LLC
 * Licensed under the Apache License, Version 2.0 (the `License`);
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an `AS IS` BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

firebase.initializeApp(config);

// Watch for state change from sign in
function initApp() {
  firebase.auth().onAuthStateChanged(user => {
    if (user) {
      // User is signed in.
      document.getElementById('signInButton').innerText = 'Sign Out';
      document.getElementById('form').style.display = '';
    } else {
      // No user is signed in.
      document.getElementById('signInButton').innerText = 'Sign In with Google';
      document.getElementById('form').style.display = 'none';
    }
  });
}
window.onload = function () {
  initApp();
};

function signIn() {
  const provider = new firebase.auth.GoogleAuthProvider();
  provider.addScope('https://www.googleapis.com/auth/userinfo.email');
  firebase
    .auth()
    .signInWithPopup(provider)
    .then(result => {
      // Returns the signed in user along with the provider's credential
      console.log(`${result.user.displayName} logged in.`);
    })
    .catch(err => {
      console.log(`Error during sign in: ${err.message}`);
      window.alert(`Sign in failed: ${err.message}`);
      accessForbidden();
    });
}

function signOut() {
  firebase
    .auth()
    .signOut()
    .then(result => {})
    .catch(err => {
      console.log(`Error during sign out: ${err.message}`);
      window.alert(`Sign out failed. Retry or check your browser logs.`);
    });
}

// Toggle Sign in/out button
function toggle() {
  if (!firebase.auth().currentUser) {
    signIn();
  } else {
    signOut();
  }
}

function accessForbidden() {
    location.href = '/noaccess'
}