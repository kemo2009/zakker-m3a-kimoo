from flask import Flask, request, redirect, session, jsonify
import json, random, urllib.parse, os
app = Flask(__name__)
app.secret_key = "kimo123"
F="users.json"
V="videos.json"
ADMIN_PASS="kimo123" # غيرها انت بعدين

def load():
    try: return json.load(open(F,encoding="utf-8"))
    except: return {}
def save(u): json.dump(u,open(F,"w",encoding="utf-8"),ensure_ascii=False)
def load_v():
    try: return json.load(open(V,encoding="utf-8"))
    except: return {}
def save_v(v): json.dump(v,open(V,"w",encoding="utf-8"),ensure_ascii=False)
CODES={}
SEO="<title>منصة زاكر مع كيمو - أولى وتانية وتالتة ثانوي عام وبكالوريا</title><meta name='description' content='منصة زاكر مع كيمو - شرح كامل لكل مواد أولى وتانية وتالتة ثانوي عام وبكالوريا'><meta name='keywords' content='منصة زاكر مع كيمو, زاكر مع كيمو, ثانوية عامة, بكالوريا'><link rel='manifest' href='/manifest.json'>"
CSS="*{box-sizing:border-box}body{margin:0;font-family:system-ui;background:#F8F7FF;direction:rtl}.header{background:linear-gradient(135deg,#7C3AED,#EC4899);color:white;text-align:center;padding:28px 16px 55px;border-radius:0 0 28px 28px}.card{background:white;margin:-28px 16px 12px;padding:16px;border-radius:18px;box-shadow:0 8px 20px rgba(0,0,0,.08)}.grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;padding:6px 16px 30px}.item{background:white;border-radius:20px;padding:20px 10px;text-align:center;box-shadow:0 4px 14px rgba(0,0,0,.06);text-decoration:none;color:#111;display:block}.item b{font-size:18px;display:block}.item span{color:#777;font-size:13px}input{width:100%;padding:14px;margin:8px 0;border:1.5px solid #ddd;border-radius:12px;font-size:17px}.btn{background:#7C3AED;color:white;border:0;padding:14px;width:100%;border-radius:12px;font-size:18px;font-weight:700;display:block;text-align:center;text-decoration:none}.btn2{background:#FF0000;color:white;padding:13px;border-radius:12px;display:block;text-align:center;text-decoration:none;font-weight:700;margin-top:8px}.btn3{background:#059669;color:white;padding:13px;border-radius:12px;display:block;text-align:center;text-decoration:none;font-weight:700;margin-top:8px}.lesson{background:white;margin:10px 16px;padding:16px;border-radius:16px;box-shadow:0 4px 12px rgba(0,0,0,.06)}"
def page(t,s,b,back="/"):
    return f"<html><head><meta name='viewport' content='width=device-width,initial-scale=1'>{SEO}<style>{CSS}</style></head><body><div class='header'><h1>{t}</h1><p>{s}</p></div><div style='padding:12px 14px'><a href='{back}' style='text-decoration:none'>⬅ رجوع</a> | <a href='/install' style='text-decoration:none'>📱 نزل التطبيق</a></div>{b}<div style='text-align:center;padding:20px;color:#888;font-size:13px'>منصة زاكر مع كيمو © 2026 | <a href='/admin'>لوحة تحكم المعلم</a></div></body></html>"
def cards(items): return '<div class="grid">'+"".join([f'<a class="item" href="{l}"><div style="font-size:38px">{e}</div><b>{n}</b><span>{d}</span></a>' for n,e,l,d in items])+"</div>"

# المنهج الكامل
L={
"1_اللغة العربية":["الجملة الاسمية","الجملة الفعلية","كان واخواتها","ان واخواتها","البلاغة: التشبيه","البلاغة: الاستعارة","الأدب: العصر الجاهلي","الأدب: العصر الاسلامي","النصوص والقراءة","التعبير"],
"1_العلوم المتكاملة":["الماء","الهواء","الطاقة والبيئة","الكائنات الحية","التغيرات الكيميائية","الأرض والفضاء","الكهرباء والمغناطيسية","الصحة والتغذية"],
"2bac_الفيزياء":["متجهات السرعة","السرعة النسبية","حركة المقذوفات الأفقية","حركة المقذوفات بزاوية","عزم القوة","اتزان القوى","القدرة والكفاءة","كمية التحرك والدفع","حفظ كمية الحركة","الحركة الدائرية","قوانين كبلر","الحركة التوافقية","الموجات والتداخل","تأثير دوبلر","العدسات","تجربة الشق المزدوج"],
"3_الفيزياء":["التيار الكهربي - قانون أوم","قانونا كيرشوف","التأثير المغناطيسي للتيار","الحث الكهرومغناطيسي","دوائر التيار المتردد","الفيزياء الحديثة","أطياف الذرة","الليزر","الالكترونيات"],
"3_الأحياء":["الدعامة والحركة","التنسيق الهرموني","التكاثر","التكاثر في النبات والانسان","المناعة","DNA","تخليق البروتين","الأحياء وعلوم الأرض"],
"3_الكيمياء":["العضوية - الهيدروكربونات","الكحولات والاحماض","الاتزان الكيميائي","الكيمياء الكهربية","الحديد","التحليل الكيميائي"],
"3_الرياضيات":["الاشتقاق","التكامل","المتتاليات","الهندسة الفراغية","المتجهات","الاحتمالات"],
}
GENERIC={"اللغة العربية":["النحو: الجملة الاسمية","البلاغة: التشبيه","الأدب: الجاهلي","النصوص","التعبير"],"اللغة الأجنبية الأولى":["المضارع","الماضي","المستقبل","المبني للمجهول","الترجمة","البراجراف"],"التاريخ":["الحضارة المصرية","الدولة الاسلامية","الحملة الفرنسية","محمد علي","ثورة 1919","ثورة 1952","حرب اكتوبر"],"الرياضيات":["الجبر","الدوال","حساب المثلثات","النهايات","الاشتقاق","التكامل"],"الفيزياء":["الميكانيكا","الموجات","الضوء","الكهرباء","المغناطيسية","الحديثة"],"الكيمياء":["المول","بنية الذرة","الجدول الدوري","الروابط","العضوية","الاتزان"],"الأحياء":["الدعامة","الهرمونات","التكاثر","المناعة","DNA"],"الجغرافيا":["موقع مصر","التضاريس","السكان","الموارد","المشكلات البيئية"],"علم النفس":["تعريف علم النفس","النمو","الذاكرة","الشخصية","الصحة النفسية"],"المحاسبة":["مقدمة المحاسبة","القيد المزدوج","اليومية","القوائم المالية","الميزانية"],"إدارة الأعمال":["الادارة","التخطيط","التسويق","الموارد البشرية","ريادة الأعمال"],"الإحصاء":["جمع البيانات","المتوسط","الاحتمالات","التوزيعات"]}
def get_lessons(lvl,mat):
    k=f"{lvl}_{mat}"
    if k in L: return L[k]
    if mat in GENERIC: return GENERIC[mat]
    return [f"الدرس {i+1}: {mat}" for i in range(8)]

G1=["اللغة العربية","التاريخ المصري","الرياضيات","العلوم المتكاملة","الفلسفة والمنطق","اللغة الأجنبية الأولى","التربية الدينية","اللغة الأجنبية الثانية","البرمجة والذكاء الاصطناعي","التربية الرياضية"]
BAC={"طب وعلوم الحياة":["اللغة العربية","اللغة الأجنبية الأولى","التاريخ","الفيزياء","الرياضيات"],"هندسة وعلوم الحاسب":["اللغة العربية","اللغة الأجنبية الأولى","التاريخ","البرمجة والذكاء الاصطناعي","الرياضيات"],"الأعمال":["اللغة العربية","اللغة الأجنبية الأولى","التاريخ","المحاسبة","إدارة الأعمال"],"الآداب والفنون":["اللغة العربية","اللغة الأجنبية الأولى","التاريخ","علم النفس","اللغة الأجنبية الثانية"]}
G2G={"علمي":["اللغة العربية","اللغة الأجنبية الأولى","التاريخ","الرياضيات","الكيمياء","الفيزياء"],"أدبي":["اللغة العربية","اللغة الأجنبية الأولى","التاريخ","الجغرافيا","علم النفس"]}
G3={"علمي علوم":["اللغة العربية","اللغة الأجنبية الأولى","الأحياء","الكيمياء","الفيزياء"],"علمي رياضة":["اللغة العربية","اللغة الأجنبية الأولى","الرياضيات","الكيمياء","الفيزياء"],"أدبي":["اللغة العربية","اللغة الأجنبية الأولى","التاريخ","الجغرافيا","الإحصاء"]}

@app.route("/manifest.json")
def manifest(): return jsonify({"name":"منصة زاكر مع كيمو","short_name":"زاكر مع كيمو","start_url":"/","display":"standalone","background_color":"#7C3AED","theme_color":"#7C3AED"})
@app.route("/sitemap.xml")
def sitemap():
    return "<?xml version='1.0'?><urlset xmlns='http://www.sitemaps.org/schemas/sitemap/0.9'><url><loc>https://zakerm3akimo.com/</loc></url><url><loc>https://zakerm3akimo.com/grade1</loc></url><url><loc>https://zakerm3akimo.com/grade2</loc></url><url><loc>https://zakerm3akimo.com/grade3</loc></url></urlset>",200,{"Content-Type":"application/xml"}
@app.route("/robots.txt")
def robots(): return "User-agent: *\nAllow: /\nSitemap: https://zakerm3akimo.com/sitemap.xml"
@app.route("/install")
def install(): return page("نزل التطبيق 📱","ذاكر مع كيمو كتطبيق",f"<div class='card'><h3>ازاي تنزل المنصة كتطبيق؟</h3><p><b>أندرويد:</b> دوس على الـ 3 نقط في كروم فوق -> Add to Home Screen / تثبيت التطبيق<br><br><b>آيفون:</b> دوس Share -> Add to Home Screen</p><p>هتلاقي أيقونة زاكر مع كيمو على موبايلك زي أي تطبيق</p><a class='btn' href='/'>ارجع للمنصة</a></div>","/")
@app.route("/")
def home():
    if "phone" not in session: return redirect("/login")
    u=load()
    return page("منصة زاكر مع كيمو 🎓",f"أهلا {u.get(session['phone'],{}).get('name','')} - عندنا {len(u)} طالب",cards([("أولى ثانوي","📚","/grade1","10 مواد"),("تانية ثانوي","📘","/grade2","عام + بكالوريا"),("تالتة ثانوي","🎓","/grade3","عام + بكالوريا")]),"/logout")
@app.route("/register",methods=["GET","POST"])
def reg():
    if request.method=="POST":
        n=request.form.get("name",""); p=request.form.get("phone","").strip(); pw=request.form.get("pw",""); u=load()
        if p in u and u[p].get("pw"): return page("تسجيل","الرقم متسجل",f"<div class='card'>متسجل قبل كده <a href='/login'>دخول</a></div>","/login")
        u[p]={"name":n,"pw":pw}; save(u); session["phone"]=p; return redirect("/")
    return page("إنشاء حساب - زاكر مع كيمو","سجل مرة واحدة",f"<div class='card'><form method='post'><input name='name' placeholder='الاسم الرباعي' required><input name='phone' placeholder='رقم الموبايل' required><input name='pw' type='password' placeholder='كلمة السر' required><button class='btn'>إنشاء حساب</button></form><p style='text-align:center'><a href='/login'>عندك حساب؟ سجل دخول</a></p></div>","/login")
@app.route("/login",methods=["GET","POST"])
def log():
    if request.method=="POST":
        p=request.form.get("phone","").strip(); pw=request.form.get("pw",""); u=load()
        if p in u and u[p].get("pw")==pw: session["phone"]=p; return redirect("/")
        return page("دخول","كلمة السر غلط",f"<div class='card'>غلط <a href='/login'>حاول تاني</a></div>","/login")
    return page("تسجيل دخول - زاكر مع كيمو","ادخل برقمك",f"<div class='card'><form method='post'><input name='phone' placeholder='رقم الموبايل' required><input name='pw' type='password' placeholder='كلمة السر' required><button class='btn'>دخول</button></form><p style='text-align:center'><a href='/register'>عمل حساب جديد</a> | <a href='/forgot'>نسيت كلمة السر؟</a></p></div>","/")
@app.route("/forgot",methods=["GET","POST"])
def forgot():
    if request.method=="POST":
        p=request.form.get("phone","").strip(); code=str(random.randint(100000,999999)); CODES[p]=code
        return page("نسيت كلمة السر","اكتب الكود",f"<div class='card'><h2 style='text-align:center;font-size:32px'>{code}</h2><form method='post' action='/reset'><input type='hidden' name='phone' value='{p}'><input name='code' placeholder='اكتب الكود' required><input name='pw' type='password' placeholder='كلمة سر جديدة' required><button class='btn'>تغيير</button></form></div>","/login")
    return page("نسيت كلمة السر","اكتب رقمك",f"<div class='card'><form method='post'><input name='phone' placeholder='رقم الموبايل' required><button class='btn'>ابعت الكود</button></form></div>","/login")
@app.route("/reset",methods=["POST"])
def reset():
    p=request.form.get("phone","").strip(); c=request.form.get("code",""); pw=request.form.get("pw","")
    if CODES.get(p)==c:
        u=load()
        if p not in u: u[p]={"name":"","pw":pw}
        else: u[p]["pw"]=pw
        save(u); session["phone"]=p; return redirect("/")
    return "الكود غلط <a href='/forgot'>حاول تاني</a>"
@app.route("/logout")
def logout(): session.clear(); return redirect("/login")

# ===== لوحة تحكمك انت بس - من غير Termux =====
@app.route("/admin",methods=["GET","POST"])
def admin():
    if request.method=="POST":
        if request.form.get("pass")!=ADMIN_PASS: return "كلمة سر الأدمن غلط"
        session["admin"]=True
    if not session.get("admin"):
        return page("لوحة تحكم المعلم 🔐","للمعلم فقط - كيمو",f"<div class='card'><form method='post'><input name='pass' type='password' placeholder='كلمة سر الأدمن' required><button class='btn'>دخول لوحة التحكم</button></form></div>","/")
    u=load(); v=load_v()
    html=f"<div class='card'><h3>📊 إحصائيات</h3><p>عدد الطلاب: <b>{len(u)}</b> | فيديوهاتك: <b>{len(v)}</b></p></div>"
    html+=f"<div class='card'><h3>➕ أضف فيديو جديد</h3><form method='post' action='/admin/add'><input name='lvl' placeholder='السنة: 1 أو 2 أو 3 أو 2bac أو 3bac' required><input name='mat' placeholder='المادة: الفيزياء' required><input name='lesson' placeholder='اسم الدرس: قانون أوم' required><input name='link' placeholder='لينك فيديو اليوتيوب' required><button class='btn'>نشر الفيديو فورا 🚀</button></form></div>"
    html+="<div class='card'><h3>🎥 فيديوهاتك</h3>"
    for k,val in v.items(): html+=f"<p><b>{k}</b> - <a href='{val}' target='_blank'>شوف الفيديو</a> - <a href='/admin/del/{urllib.parse.quote(k)}'>🗑 مسح</a></p>"
    html+="</div><div class='card'><h3>👥 الطلاب</h3>"
    for ph,info in u.items(): html+=f"<p>{info.get('name','')} - {ph}</p>"
    html+="</div>"
    return page("لوحة تحكم كيمو 🔐","انت المتحكم هنا",html,"/")
@app.route("/admin/add",methods=["POST"])
def admin_add():
    if not session.get("admin"): return redirect("/admin")
    v=load_v(); key=f"{request.form.get('lvl')}_{request.form.get('mat')}_{request.form.get('lesson')}"
    v[key]=request.form.get("link"); save_v(v); return redirect("/admin")
@app.route("/admin/del/<key>")
def admin_del(key):
    if not session.get("admin"): return redirect("/admin")
    v=load_v(); k=urllib.parse.unquote(key)
    if k in v: del v[k]; save_v(v)
    return redirect("/admin")

@app.route("/grade1")
def g1(): return page("أولى ثانوي - زاكر مع كيمو","10 مواد",cards([(m,"📖",f"/subject/1/{m}","دروس + فيديوهات") for m in G1]),"/")
@app.route("/grade2")
def g2(): return page("تانية ثانوي","اختار النظام",cards([("ثانوي عام","📘","/g2general","علمي و أدبي"),("بكالوريا","🎓","/g2bac","4 مسارات")]),"/")
@app.route("/g2general")
def g2g(): return page("تانية ثانوي عام","اختار الشعبة",cards([("علمي","🔬","/g2g/علمي","6 مواد"),("أدبي","📚","/g2g/أدبي","5 مواد")]),"/grade2")
@app.route("/g2g/<sec>")
def g2g2(sec): return page(f"تانية عام - {sec}","مواد الشعبة",cards([(m,"📖",f"/subject/2/{m}","دروس + فيديوهات") for m in G2G[sec]]),"/g2general")
@app.route("/g2bac")
def g2b(): return page("تانية بكالوريا","اختار المسار",cards([(k,"🎯",f"/g2bac/{k}","5 مواد") for k in BAC]),"/grade2")
@app.route("/g2bac/<track>")
def g2b2(track): return page(f"تانية بكالوريا - {track}","مواد المسار",cards([(m,"📖",f"/subject/2bac/{m}","دروس + فيديوهات") for m in BAC[track]]),"/g2bac")
@app.route("/grade3")
def g3(): return page("تالتة ثانوي","اختار النظام",cards([("ثانوي عام","📘","/g3general","3 شعب"),("بكالوريا","🎓","/g3bac","4 مسارات")]),"/")
@app.route("/g3general")
def g3g(): return page("تالتة ثانوي عام","اختار الشعبة",cards([(k,"🎯",f"/g3g/{k}","5 مواد") for k in G3]),"/grade3")
@app.route("/g3g/<sec>")
def g3g2(sec): return page(f"تالتة عام - {sec}","مواد الشعبة",cards([(m,"📖",f"/subject/3/{m}","دروس + فيديوهات") for m in G3[sec]]),"/g3general")
@app.route("/g3bac")
def g3b(): return page("تالتة بكالوريا","اختار المسار",cards([(k,"🎯",f"/g3bac/{k}","مواد متقدمة") for k in BAC]),"/grade3")
@app.route("/g3bac/<track>")
def g3b2(track): return page(f"تالتة بكالوريا - {track}","مواد المسار",cards([(m,"📖",f"/subject/3bac/{m}","دروس + فيديوهات") for m in BAC[track]]),"/g3bac")
@app.route("/subject/<lvl>/<mat>")
def subj(lvl,mat):
    lessons=get_lessons(lvl,mat); v=load_v()
    html=f"<div class='card'><h3>📖 كتاب الوزارة - {mat}</h3><a class='btn3' href='https://books.moe.gov.eg' target='_blank'>افتح كتب الوزارة</a></div>"
    html+=f"<div class='card'><h3>🎥 دروس {mat} - المنهج الكامل ({len(lessons)} درس)</h3></div>"
    for les in lessons:
        key=f"{lvl}_{mat}_{les}"
        custom=v.get(key)
        if custom:
            html+=f"<div class='lesson'><b>{les} ⭐ فيديو كيمو</b><a class='btn2' href='{custom}' target='_blank'>▶ شاهد فيديو كيمو</a></div>"
        else:
            q=urllib.parse.quote(f"شرح {les} {mat} ثانوي")
            yt=f"https://www.youtube.com/results?search_query={q}"
            html+=f"<div class='lesson'><b>{les}</b><a class='btn2' href='{yt}' target='_blank'>▶ شاهد الشرح على يوتيوب</a></div>"
    return page(mat,f"{len(lessons)} درس",html,"/")
if __name__=="__main__":
    port=int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0",port=port)
