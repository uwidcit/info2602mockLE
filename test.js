const puppeteer = require('puppeteer');
const { expect, assert }  = require('chai');


let URL ="http://127.0.0.1:8080/app";
const HEADLESS = true;
const TIMEOUT = 12000;

let browser;
let page;

before(async function(){
    this.timeout(TIMEOUT);
    browser = await puppeteer.launch({ headless: HEADLESS,  defaultViewport: null,  args: ['--no-sandbox', '--disable-setuid-sandbox']});
    page = await browser.newPage();
    await page.emulateMedia("screen");
    await page.goto(URL, { waitUntil: 'networkidle2'});
});

function getInnerText(selector){
  return page.evaluate(selector=>document.querySelector(selector).innerText, selector);
}


function checkElements(elements){
  for(let [name, ele] of Object.entries(elements)){
    it(`Should have ${name}`, async()=>{
      expect(await page.$(ele)).to.be.ok;
    });
  }
}

describe('Test Suite 1: Page should have the appropriate title', ()=>{
  it('Check for the "Document" title', async()=>{
    expect(await page.title()).to.eql('Document');
  });
});


after(async () => {
  await browser.close();
});