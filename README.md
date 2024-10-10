# HM-Surf evaluator
Evaluates susceptibility to [CVE-2024-44133](https://nvd.nist.gov/vuln/detail/CVE-2024-44133) of common macOS browsers.  
Also contains the HTML that takes a screenshot and downloads it along with location extraction.
![Screenshot](screenshot.png)

## Usage - evaluator
To run the evaluator, which evaluates [CVE-2024-44133](https://nvd.nist.gov/vuln/detail/CVE-2024-44133) on all common macOS browsers, run:

```shell
python3 -m pip install -r ./requirements.txt
./hm-surf-eval.py
```

Upon execution, the tool evaluates TCC bypassing capabilities of all common macOS browsers.

## Usage - HTML
The file [hm-surf.html] is an example HTML page that demontrates [CVE-2024-44133](https://nvd.nist.gov/vuln/detail/CVE-2024-44133).  
All it does is access the camera and location, presenting the location (with low accuracy, on purpose) and downloads the camera screenshot (but it could just as easily save it on a server).  
This file is *not* an exploit by itself, and requires Camera, Microphone and location access enabled for the browser, e.g. by a local attacker overriding the per-browser preferences.  
That capability can be assessed with the evaluator.  
To view the HTML page easily, you could use any tool, e.g. [htmlpreview](http://htmlpreview.github.io/?https://github.com/yo-yo-yo-jbo/hm-surf/blob/main/hm-surf.html).
