// import { GlobalState } from "./main";

export function run() {
  document.addEventListener("htmx:after-swap", (event: any) => {
    if (!(event.target instanceof HTMLElement)) {
      return;
    }
    else if (event.detail.pathInfo.requestPath == "/basket") {
      return;
    }
    else if (event.detail.pathInfo.requestPath == "/komentarisanje/") {
      return;
    }
    else if (event.detail.pathInfo.requestPath == "/ocenjivanje") {
      //@ts-ignore
      Alpine.store('all').modal.toggle();
      document.querySelector("#ratings")?.scrollIntoView();
      return;
    }

    window.scrollTo(0, 0);
  });

  document.addEventListener("htmx:beforeSwap", (event: any) => {
    if (event.detail.xhr.responseURL.includes('log-user')) {
      if (event.detail.xhr.response.includes('id=\"logged\"')) {
        // event.detail.shouldSwap = false;
        // _store().modal.setCurrent('user');
        //@ts-ignore
        Alpine.store('all').modal.toggle();
      }
      else {
        event.detail.shouldSwap = false;
      }
    }
  })

  document.addEventListener("htmx:afterRequest", (event: any) => {

    if (event.detail.xhr.responseURL.includes('narucivanje')) {
      if (event.detail.successful) {
        //@ts-ignore
        Alpine.store('all').basket.deleteAll();
        //@ts-ignore
        Alpine.store('all').basket.toDelete = true;
      }
    }
  })

  document.addEventListener("htmx:beforeRequest", (event: any) => {

    if (event.detail.requestConfig.path == "/basket") {
      //@ts-ignore
      if (Alpine.store('all').basket.toDelete == true) {
        event.detail.xhr.abort();
      }
    }
    
  });

}
