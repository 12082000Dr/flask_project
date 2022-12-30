var cards_block = document.querySelector('.cards');
var cards = document.querySelectorAll('.cards > div');

function start() {
  var random = Math.floor(Math.random() * 6); // От 0 до 7
  cards_block.style.left = -random * 100 + 'px';
  setTimeout(function() {
    random++;
    cards[random].style.background = '#7B90F7';
    cards[random].style.color = 'white';
  }, 5000)
}