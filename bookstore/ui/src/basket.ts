type GlobalBasket = {sum: number}

export function basketData(cena: number, count: number) {
  return {
    cena,
    count,
    deleted: false,
    s() { return this.cena * this.count; },
    ukupno() {
      return `Ukupno: ${this.s().toFixed(2)} din`
    },
    all() {
      return `Komada: ${this.count}`
    },
    del(el: HTMLElement) {
      el.classList.toggle('deleted_book');
      //@ts-ignore
      this.sum -= this.s();
      setTimeout(() => { el.remove() }, 1700);
    },
    decr(basket: GlobalBasket) {
      if (this.count > 1) {
        this.count -= 1;
        //@ts-ignore
        basket.sum -= cena;
      }
    },
    incr(basket: GlobalBasket) {
      this.count += 1;
      //@ts-ignore
      basket.sum += cena;
    }
  }
}