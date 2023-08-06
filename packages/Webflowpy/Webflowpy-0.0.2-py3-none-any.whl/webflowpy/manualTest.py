from webflowpy.Webflow import Webflow

if __name__ == "__main__":
    webflow = Webflow()

    webflow.info()
    webflow.site('5c2601f89a1575861286a249')
    webflow.collections('5c2601f89a1575861286a249')
    webflow.collection('5c26497f4fdbbae398c05031')
    webflow.items('5c26497f4fdbbae398c05031')