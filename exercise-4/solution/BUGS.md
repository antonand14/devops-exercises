# Solution notes
# Bug 1 (manifest): deployment injects the env var as APP_MESSAGE but app.py reads os.environ["MESSAGE"] — KeyError on every request → CrashLoopBackOff
# Fix: change os.environ["MESSAGE"] to os.environ["APP_MESSAGE"] in app.py (or rename the env var in the deployment to MESSAGE)
# Bug 2 (Python): none additional — the single bug is the env var name mismatch
