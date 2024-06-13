# CVaR and loss cover selection

In previous exercises you saw that both the** ****T** and the** ****Gaussian KDE**distributions fit portfolio losses for the crisis period fairly well. Given this, which of these is best for** ** *risk management* ? One way to choose is to select the distribution that provides the largest** ** *loss cover* , to cover the "worst worst-case scenario" of losses.

The** **`t` and** **`kde` distributions are available and have been fit to 2007-2008 portfolio** **`losses` (`t` fitted parameters are in** **`p`). You'll derive the one day 99% CVaR estimate for each distribution; the largest CVaR estimate is then the 'safest'** ****reserve amount** to hold, covering expected losses that exceed the 99% VaR.

The** **`kde` instance has been given a special** **`.expect()` method,** ** *just for this exercise* , to compute the expected value needed for the CVaR.
