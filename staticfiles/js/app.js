const cards = document.querySelectorAll('.wing_card');

cards.forEach(card => {
  const glow = card.querySelector('.glow');

  card.addEventListener('mousemove', (e) => {
    const rect = card.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    // Apply glow movement
    if (glow) {
      glow.style.top = `${y}px`;
      glow.style.left = `${x}px`;
    }

    const centerX = rect.width / 2;
    const centerY = rect.height / 2;
    const rotateX = ((y - centerY) / centerY) * 10;
    const rotateY = ((x - centerX) / centerX) * -10;

    card.style.transform = `rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
  });

  card.addEventListener('mouseleave', () => {
    card.style.transform = `rotateX(0deg) rotateY(0deg)`;
    if (glow) {
      glow.style.top = `50%`;
      glow.style.left = `50%`;
    }
  });
});


gsap.registerPlugin(ScrollTrigger);

// Using Locomotive Scroll from Locomotive https://github.com/locomotivemtl/locomotive-scroll

const locoScroll = new LocomotiveScroll({
  el: document.querySelector(".main"),
  smooth: true
});
// each time Locomotive Scroll updates, tell ScrollTrigger to update too (sync positioning)
locoScroll.on("scroll", ScrollTrigger.update);

// tell ScrollTrigger to use these proxy methods for the ".main" element since Locomotive Scroll is hijacking things
ScrollTrigger.scrollerProxy(".main", {
  scrollTop(value) {
    return arguments.length ? locoScroll.scrollTo(value, 0, 0) : locoScroll.scroll.instance.scroll.y;
  }, // we don't have to define a scrollLeft because we're only scrolling vertically.
  getBoundingClientRect() {
    return {top: 0, left: 0, width: window.innerWidth, height: window.innerHeight};
  },
  // LocomotiveScroll handles things completely differently on mobile devices - it doesn't even transform the container at all! So to get the correct behavior and avoid jitters, we should pin things with position: fixed on mobile. We sense it by checking to see if there's a transform applied to the container (the LocomotiveScroll-controlled element).
  pinType: document.querySelector(".main").style.transform ? "transform" : "fixed"
});





// each time the window updates, we should refresh ScrollTrigger and then update LocomotiveScroll. 
ScrollTrigger.addEventListener("refresh", () => locoScroll.update());

// after everything is set up, refresh() ScrollTrigger and update LocomotiveScroll because padding may have been added for pinning, etc.
ScrollTrigger.refresh();

setTimeout(() => {
  scroll.update(); // after data is fully in DOM
}, 1000);

var app = document.getElementById('app');

var typewriter = new Typewriter(app, {
    loop: true
});

typewriter.typeString('<b>CODE CONNECT CREATE</b>')
    .pauseFor(1500)
    .deleteAll()
    .typeString('<b>LREAN TODAY,LEAD TOMORROW</b>')
    .pauseFor(1500)
    .deleteAll()
    .typeString('<b>WHERE CODER BECOME CREATORS</b> ')
    .pauseFor(1500)
    .start();




$(document).ready(function () {
  // Load previously opened FAQ from localStorage
  const openId = localStorage.getItem("openFaqId");
  if (openId) {
    const $item = $(`.faq-item[data-id="${openId}"]`);
    $item.addClass("active");
    $item.find(".faq-answer").slideDown();
  }

  $(".faq-question").on("click", function () {
    const $item = $(this).closest(".faq-item");

    // Collapse all others
    $(".faq-item").not($item).removeClass("active").find(".faq-answer").slideUp();

    // Toggle this one
    $item.toggleClass("active");
    $item.find(".faq-answer").slideToggle();

    // Save to localStorage if open
    if ($item.hasClass("active")) {
      localStorage.setItem("openFaqId", $item.data("id"));

      // Scroll smoothly to opened FAQ

    } else {
      localStorage.removeItem("openFaqId");
    }
  });
});


gsap.to(".loader",{
  y:-1000,
  duration:1,
  ease:"power1.inOut",
  delay:.4,
})

gsap.from(".text_content",{
  y:100,
  duration:.6,
  ease:"power1.inOut",
  delay:.6,
})


  gsap.registerPlugin(ScrollTrigger);

gsap.to(".mission_one", {
  scale: 1,
  opacity: 1,
  stagger: 0.4,
  scrollTrigger: {
    scroller: ".main",

    trigger: ".vision_section_warper",
    start: "top 70%",
    end: "top 40%",
    scrub: 3
  }
});
gsap.to(".wing_card",{
  scale: 1,
  opacity: 1,
  stagger: 0.4,
  scrollTrigger: {
    scroller: ".main",
    trigger: ".wing_card_wapper",
    start: "top 90%",
    end: "top 70%",
    scrub: 3
  }
  
})

gsap.from(".events_warper",{
  scale: .8,
  opacity: 0,
  scrollTrigger: {
    scroller: ".main",
    trigger: ".events_warper",
    start: "top 90%",
    end: "top 70%",
    scrub: 3
  }
  
})
gsap.from(".projects_wrapper",{
  scale: .8,
  opacity: 0,
  scrollTrigger: {
    scroller: ".main",
    trigger: ".projects_wrapper",
    start: "top 90%",
    end: "top 70%",
    scrub: 3
  }
  
})
gsap.from(".faq_warper",{
  scale: .8,
  opacity: 0,
  scrollTrigger: {
    scroller: ".main",
    trigger: ".faq_warper",
    start: "top 90%",
    end: "top 70%",
    scrub: 3
  }
  
})


gsap.from(".vision_mision",{
  scale: .8,
  opacity: 0,
  delay:.6,
  duration:1,
})
gsap.from(".announcement_box",{
  scale: .8,
  opacity: 0,
  delay:.6,
  duration:1,
})


// resposive menu js 
const menu = document.getElementById("menu");
const sideMenu = document.getElementById("sideMenu");
const closeMenu = document.getElementById("closeMenu");

menu.onclick = () => {
  sideMenu.style.width = "70%";
};

closeMenu.onclick = () => {
  sideMenu.style.width = "0";
};





// security site 
document.addEventListener('contextmenu', e => e.preventDefault());
document.onkeydown = function(e) {
  if (e.key == "F12" || (e.ctrlKey && e.shiftKey && e.key == "I")) {
    return false;
  }
};

document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("contact-form");
  const successMessage = document.getElementById("success-message");
  const errorMessage = document.getElementById("error-message");
  const submitButton = document.getElementById("submit-button");

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    const formData = new FormData(form);
    let isMalicious = false;

    for (let [key, value] of formData.entries()) {
      if (typeof value === 'string' && /<script.*?>.*?<\/script>/gi.test(value)) {
        isMalicious = true;
        break;
      }
    }

    if (isMalicious) {
      errorMessage.innerHTML = "Don't do this brother 😡";
      errorMessage.style.display = "block";
      successMessage.style.display = "none";
      submitButton.textContent = "Send Message";
      return;
    }

    const originalText = submitButton.textContent;
    submitButton.textContent = "Sending...";

    fetch("", {
      method: "POST",
      headers: {
        "X-CSRFToken": formData.get("csrfmiddlewaretoken"),
        "X-Requested-With": "XMLHttpRequest"
      },
      body: formData
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        successMessage.textContent = data.message;
        successMessage.style.display = "block";
        errorMessage.style.display = "none";
        form.reset();
        submitButton.textContent = "Sended ✅";
      } else {
        errorMessage.innerHTML = '';
        for (const field in data.errors) {
          errorMessage.innerHTML += `${field}: ${data.errors[field].join(', ')}<br>`;
        }
        errorMessage.style.display = "block";
        successMessage.style.display = "none";
        submitButton.textContent = "Sorry ❌";
      }
    })
    .catch(error => {
      console.error("Error:", error);
      submitButton.textContent = "Sorry ❌";
    })
    .finally(() => {
      setTimeout(() => {
        submitButton.textContent = originalText;
      }, 3000);
    });
  });
});