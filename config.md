Options are organized by *collection* and *deck options*.

* *straightLength*: Length of what is considered a straight success. At this length, ease rewards will be applied. The value is the same as deactivating Straight Rewards. (default: 0)
* *enableNotifications*: Whether notifications / tooltips are shown during review. (default: true)
* *baseEase*: One of the two values for calculating the ease reward. (default: 15)
* *stepEase*: One of the two values for calculating the ease reward. (default: 5)
* *startEase*: Only cards with an ease factor between (inclusive) "Start Ease" and "Stop Ease" are considered for ease rewards. (default: 130)
* *stopEase*: Only cards with an ease factor between (inclusive) "Start Ease" and "Stop Ease" are considered for ease rewards. (default: 250)

The formula for calculating the ease reward is:

    if straightLength >= requiredStraightLength:
      baseEase + stepEase ⋅ (straightLength - requiredStraightLength)
    else:
      0
