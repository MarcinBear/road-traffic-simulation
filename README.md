# road-traffic-simulation 🚦🟦🟦🟦
---

### Dash app designed to simulate a fictional road traffic (on a fixed map) based on inhomogeneous Poisson processes.

❯❯❯❯❯  **App deployed on Heroku: https://road-traffic-simulation.herokuapp.com/** *(Note: it may take a while for the app to wake up)*

---

![app_screenshot_error](images/website_screenshot1.png "app screenshot")
<p align="center">website screenshot<p>
  
---

![app_screenshot2_error](images/website_screenshot2.png "app screenshot 2")
<p align="center">website screenshot<p>
  
---
  
Each beginning of the road marked with a capital letter generates new cars at the arrival moments of the corresponding inhomogeneous poisson process. Intensity functions of processes are listed below. 
  
* `λ₁(t) = 0.8 + 0.8 * sin(t/2)`

* `λ₂(t) = exp((2 * sin(t/12 + 3) - 0.9)^3)`
 
* `λ₃(t) = 0.5`
  
* `λ₄(t) = 0.7 + 0.6 * sin(t/7 + 2)^2 * cos(t/3 + 1)`
  
* `λ₅(t) = 0.2 + 0.2 * sign(sin(t/24 + 6))`
  
* `λ₆(t) = 0.1 + 0.1 * sin(sqrt(t))`
  
* `λ₇(t) = 0.3 + 0.3 * sin(4 * sin(t/2))`

---

 ### Parameters
  
🟦

🟦
 
 ---
