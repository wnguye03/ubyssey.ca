const months = ["Jan.", "Feb.", "March", "April", "May", "June", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."];

export function formatPubDate(date) {
  if (!date) { return date; }
  const dateObj = new Date(date);
  const hours24 = dateObj.getHours();

  const dateString = `${months[dateObj.getMonth()]} ${dateObj.getDate()}, ${dateObj.getFullYear()}`;

  const ampm = hours24 < 12 ? 'a.m.' : 'p.m.';

  let hour;
  if (hours24 < 12) {
      hour = hours24 == 0 ? '12' : ('' + hours24);
  } else {
      hour = '' + (hours24 - 11);
  }

  const minute = ('00' + dateObj.getMinutes()).slice(-2);  // zero-pad

  return `${dateString}, ${hour}:${minute} ${ampm}`;
}
