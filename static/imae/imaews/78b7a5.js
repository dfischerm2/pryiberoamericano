try {
    !function (e, t, n) {
        var o = "lazyLoadXT", r = o + "_lazied", a = "load error", i = t.documentElement || t.body, l = {
            autoInit: !0,
            preload: !0,
            selector: "img[data-src]",
            blankImage: "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7",
            throttle: 99,
            forceLoad: e.onscroll === n || !!e.operamini || !i.getBoundingClientRect,
            loadEvent: "pageshow",
            updateEvent: "load orientationchange resize scroll touchmove focus",
            forceEvent: "lazyloadall",
            oninit: {removeClass: "lazy"},
            onshow: {addClass: "lazy-hidden"},
            onload: {removeClass: "lazy-hidden", addClass: "lazy-loaded"},
            onerror: {removeClass: "lazy-hidden"},
            checkDuplicates: !0
        }, c = {srcAttr: "data-src", edgeX: 0, edgeY: 0, visibleOnly: !0}, s = [], d = 0, f = 0, u = 0;

        function g(e) {
            for (var t, n, o = 1; o < arguments.length; o++) for (n in t = arguments[o]) e[n] = t[n];
            return e
        }

        function v(e, t) {
            return e[t] === n ? l[t] : e[t]
        }

        function h() {
            var t = e.pageYOffset;
            return t === n ? i.scrollTop : t
        }

        function A(e) {
            return "function" == typeof e
        }

        function p(e) {
            return "string" == typeof e
        }

        function m(e, t) {
            if (t) for (; t = t.parentNode;) if (t === e) return !0;
            return !1
        }

        function E(e, n, o) {
            e = p(e) ? t.querySelectorAll(e) : [e], n = n.split(" ");
            for (var r, a = 0; a < e.length; a++) for (r = 0; r < n.length; r++) e[a].addEventListener(n[r], o, {
                capture: !0,
                passive: !0
            })
        }

        function y(e, t, n) {
            t = t.split(" ");
            for (var o = 0; o < t.length; o++) e.removeEventListener(t[o], n)
        }

        function C(e, t, n) {
            if (t) {
                var o, r = 0, a = " " + e.className.replace(/[\t\r\n\f]/g, " ") + " ", i = a;
                for (t = t.match(/\S+/g) || []; r < t.length; r++) o = t[r] + " ", n ? i = i.replace(" " + o, " ") : i.indexOf(" " + o) < 0 && (i += o);
                a !== i && (e.className = i.slice(1, -1))
            }
        }

        function z(e, n) {
            var o = l["on" + e];
            o && (A(o) ? o.call(n) : (C(n, o.addClass), C(n, o.removeClass, !0))), (o = t.createEvent("Event")).initEvent("lazy" + e, !0, !0), n.dispatchEvent(o), T()
        }

        function b(e) {
            var t = e.currentTarget;
            u--, l.preload && 0 === u && L(1), y(t, a, b), z(e.type, t)
        }

        function L(t) {
            if (s.length) {
                t = t || l.forceLoad, d = 1 / 0;
                var n, c, f = h(), g = e.innerHeight || i.clientHeight, v = e.innerWidth || i.clientWidth;
                for (n = 0, c = s.length; n < c; n++) {
                    var p, y = s[n], C = y[o], L = !1, I = t < 0 || t > u || y[r] < 0;
                    if (m(i, y)) {
                        if (I || !C.visibleOnly || y.offsetWidth || y.offsetHeight) {
                            if (!I) {
                                var T = y.getBoundingClientRect(), w = C.edgeX, B = C.edgeY;
                                I = (p = T.top + f - B - g) <= f && T.bottom > -B && T.left <= v + w && T.right > -w
                            }
                            if (I) {
                                u++, E(y, a, b), z("show", y);
                                var O = C.srcAttr, k = A(O) ? O(y) : y.getAttribute(O);
                                k && (y.src = k), L = !0
                            } else p < d && (d = p)
                        }
                    } else L = !0;
                    L && (y[r] = 0, s.splice(n--, 1), c--)
                }
                c || z("complete", i)
            }
        }

        function I() {
            f > 1 ? (f = 1, L(), setTimeout(I, l.throttle)) : f = 0
        }

        function T(t) {
            s.length && (t && "scroll" === t.type && t.currentTarget === e && d >= h() || (f || setTimeout(I, 0), f = 2))
        }

        function w(e) {
            var n, a, i, l = v(e = p(e) ? {selector: e} : e || {}, "blankImage"), d = v(e, "checkDuplicates"),
                f = v(e, "scrollContainer"), u = v(e, "show"), h = {}, A = v(e, "selector"),
                m = p(A) ? t.querySelectorAll(A) : [A];
            for (n in f && E(f, "scroll", T), c) h[n] = v(e, n);
            for (n = 0; n < m.length; n++) a = m[n], i = d && a[r], a[r] = u ? -1 : 1, i || (l && "IMG" === a.tagName && !a.src && (a.src = l), a[o] = g({}, h), z("init", a), s.push(a));
            T()
        }

        function B() {
            w()
        }

        function O() {
            L(-1)
        }

        function k() {
            z("start", e), E(e, l.updateEvent, T), E(e, l.forceEvent, O), E(t, l.updateEvent, T), l.autoInit && (E(e, l.loadEvent, B), B())
        }

        g(l, c, e[o]), e[o] = w, l = g(e[o], l), g(e[o], {
            extend: g,
            isFunction: A,
            onEvent: E,
            offEvent: y,
            triggerEvent: z,
            check: T
        }), "loading" !== t.readyState ? setTimeout(k, 0) : t.addEventListener("DOMContentLoaded", k)
    }(window, document);
} catch (e) {
    console.log(e)
}
try {
    !function () {
        var t = window.lazyLoadXT;
        t.selector += ",video,iframe[data-src]", t.videoPoster = "data-poster", t.onEvent(document, "lazyshow", function (e) {
            var r = e.target;
            if ("VIDEO" === r.tagName) {
                var a = t.srcAttr, o = t.isFunction(a), i = !1, s = r.getAttribute(t.videoPoster);
                s && r.setAttribute("poster", s);
                for (var d = r.childNodes, n = 0; n < d.length; n++) {
                    var v = d[n], c = v.tagName;
                    if ("SOURCE" === c || "TRACK" === c) {
                        var u = o ? a(v) : v.getAttribute(a);
                        u && (v.setAttribute("src", u), i = !0)
                    }
                }
                i && r.load()
            }
        })
    }()
} catch (e) {
    console.log(e)
}
try {
    !function (t, e, r) {
        var s, n, i = t.lazyLoadXT, c = e.documentElement, a = "srcset" in new Image, u = /^\s*(\S+)/,
            o = /\S\s+(\d+)w/, d = /\S\s+([\d\.]+)x/, l = [0, 1 / 0], f = [0, 1], A = {
                srcsetAttr: "data-srcset",
                srcsetExtended: !0,
                srcsetBaseAttr: "data-srcset-base",
                srcsetExtAttr: "data-srcset-ext",
                srcsetSizesAttr: "data-srcset-size"
            }, x = {w: 0, x: 0};
        for (s in A) void 0 === i[s] && (i[s] = A[s]);

        function g(t, e) {
            for (var r = [], s = 0; s < t.length; s++) e(t[s]) && r.push(t[s]);
            return r
        }

        function h(t, e) {
            for (var r, s = [], n = 0; n < t.length; n++) null !== (r = e(t[n])) && s.push(r);
            return s
        }

        function w(t, e) {
            return Math[e].apply(null, h(t, function (t) {
                return t[s]
            }))
        }

        function v(t) {
            return t[s] >= x[s] || t[s] === n
        }

        function b(t) {
            return t[s] === n
        }

        function p(t) {
            return t.replace(/^\s+|\s+$/g, "").replace(/(\s+[\d\.]+[wx]),\s*|\s*,\s+/g, "$1 @,@ ").split(" @,@ ")
        }

        function m(e) {
            var r = e.getAttribute(i.srcsetAttr);
            if (!r) return !1;
            var a, A, m = h(p(r), function (t) {
                return {url: u.exec(t)[1], w: parseFloat((o.exec(t) || l)[1]), x: parseFloat((d.exec(t) || f)[1])}
            });
            if (!m.length) return !1;
            if (x = {
                w: t.innerWidth || c.clientWidth,
                x: t.devicePixelRatio || 1
            }, "auto" === e.getAttribute(i.srcsetSizesAttr)) {
                var E = e.width;
                e.width = x.w, x.w = e.scrollWidth, e.width = E
            }
            for (a in x.w *= x.x, x) s = a, n = w(m, "max"), m = g(m, v);
            for (a in x) s = a, n = w(m, "min"), m = g(m, b);
            return A = m[0].url, i.srcsetExtended && (A = (e.getAttribute(i.srcsetBaseAttr) || "") + A + (e.getAttribute(i.srcsetExtAttr) || "")), A
        }

        i.selector += ",img[" + i.srcsetAttr + "]", i.onEvent(e, "lazyshow", function (t) {
            var e = t.target;
            if ("IMG" === e.tagName) {
                var r = e.getAttribute(i.srcsetAttr);
                if (r) if (a) {
                    if (i.srcsetExtended) {
                        var s = e.getAttribute(i.srcsetBaseAttr) || "", n = e.getAttribute(i.srcsetExtAttr) || "";
                        r = p(r);
                        for (var c = 0; c < r.length; c++) {
                            var u = r[c], o = u.indexOf(" ");
                            o < 0 && (o = u.length), r[c] = s + u.substr(0, o) + n + u.substr(o)
                        }
                        r = r.join(", ")
                    }
                    e.setAttribute("srcset", r)
                } else e.lazyLoadXT.srcAttr = m
            }
        })
    }(window, document)
} catch (e) {
    console.log(e)
}
try {
    !function (e, t) {
        function n() {
            for (var i, r = t.getElementsByTagName("link"), s = 0; s < r.length; s++) if ("preload" === (i = r[s]).rel && "style" === i.getAttribute("as") || "stylesheet" === i.rel && "only x" === i.media) return setTimeout(n, 100);
            (s = t.createEvent("HTMLEvents")).initEvent("resize", !0, !1), e.dispatchEvent(s)
        }

        setTimeout(n, 100)
    }(window, document)
} catch (e) {
    console.log(e)
}