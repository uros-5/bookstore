import { basketData } from "./basket";
import { run as runHTMX } from "./htmxListener";
import { reactive } from "@vue/reactivity";

const user = {
  selected: "login",
  isLogged: false,
  username: "",
  password: "",
  setSelected(selected: string) {
    s().user.selected = selected;
  },
  setLogged(logged: boolean) {
    s().user.isLogged = logged;
  },
  reset() {
    s().user.setLogged(false);
    s().user.username = "";
    s().user.password = "";
    s().user.selected = "login";
    setTimeout(() => {
      (document.querySelector("#home") as HTMLElement).click();
    }, 500)
  }
};

const basket = {
  items: [], toDelete: false, deleteAll() {
    const btns = document.querySelectorAll(".del-btn")
    let len = btns.length;
    let count = 0;
    btns.forEach(item => {
      setTimeout(() => {
        count += 1;
       (item as HTMLElement).click(); 
        if (count == len) {
          //@ts-ignore
          Alpine.store('all').basket.toDelete = false;
          //@ts-ignore
          Alpine.store('all').modal.current = "server";
          setTimeout(() => {
            //@ts-ignore
            Alpine.store('all').modal.toggle();
          },1000)
        }
      }, 500)
    });
  }
};

const modal = {
  visible: false,
  current: "",
  setCurrent(c: string) {
    s().modal.current = c;
  },
  toggle() {
    s().modal.visible = !s().modal.visible;
    if (!s().modal.visible) this.setCurrent("");
  },
  close() {
    this.setCurrent("");
    s().modal.visible = false;
  },
};

const ratings = {
  rating: 0,
}

export type Basket = typeof basket

export type User = typeof user

export type Modal = typeof modal;

export type Ratings = typeof ratings;

export type GlobalState = {
  basket: Basket,
  user: User,
  modal: Modal,
}

export function s(): GlobalState {
  //@ts-ignore
  return Alpine.store("all");
}

export function run() {
  const state = { user, modal, basket, ratings };
  (window as any).basketData = basketData;

  document.addEventListener('alpine:init', () => {
    //@ts-ignore
    Alpine.store('all',
      reactive(state)
    );
  })
}

run()
runHTMX();
