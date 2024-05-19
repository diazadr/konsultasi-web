from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from bson.objectid import ObjectId
from config import MONGO_URI, DATABASE_NAME, COLLECTION_NAME
from pymongo.server_api import ServerApi

app = Flask(__name__)
app.secret_key = 'your_secrect_key'

client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
db = client[DATABASE_NAME]
mahasiswa_collection = db['mahasiswa_collection']
jurusan_collection = db['jurusan']
kompetensi_collection = db['kompetensi']
users_collection = db['users']
dosen_collection = db['dosen']
konsultasi_collection = db['konsultasi']

@app.route('/')
def index():
    return render_template('landing_page.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users_collection.find_one({'username': username})
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            session['user_id'] = str(user['_id'])
            session['role'] = user['role']
            flash('Login berhasil', 'success')
            return redirect(url_for('profile', username=username))
        flash('Login gagal, periksa username dan password Anda', 'danger')
    return render_template('landing_page.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        role = 'user'
        
        if users_collection.find_one({'username': username}):
            flash('Username sudah ada. Silakan pilih yang lain.', 'danger')
            return redirect(url_for('index'))

        hashed_password = generate_password_hash(password)
        user_data = {
            'name': name,
            'email': email,
            'username': username,
            'password': hashed_password,
            'role': role
        }
        users_collection.insert_one(user_data)
        flash('Registrasi berhasil', 'success')
        return redirect(url_for('index'))
    return render_template('landing_page.html')

@app.route('/list_users')
def list_users():
    if session.get('role') == 'admin':
        all_users = users_collection.find()
        return render_template('user/list_users.html', users=all_users)
    else:
        flash('You are not authorized to view this page.', 'danger')
        return redirect(url_for('index'))

@app.route('/edit_user/<user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if session.get('role') == 'admin':
        user = users_collection.find_one({'_id': ObjectId(user_id)})
        if request.method == 'POST':
            new_username = request.form['username']
            new_password = request.form['password']
            
            # Update data pengguna
            updated_data = {
                'username': new_username,
                'password': new_password
            }
            users_collection.update_one({'_id': ObjectId(user_id)}, {'$set': updated_data})
            flash('User updated successfully!', 'success')
            return redirect(url_for('list_users'))
        return render_template('user/edit_user.html', user=user)
    else:
        flash('You are not authorized to perform this action.', 'danger')
        return redirect(url_for('index'))

@app.route('/delete_user/<user_id>')
def delete_user(user_id):
    if session.get('role') == 'admin':
        users_collection.delete_one({'_id': ObjectId(user_id)})
        flash('User deleted successfully!', 'success')
        return redirect(url_for('list_users'))
    else:
        flash('You are not authorized to perform this action.', 'danger')
        return redirect(url_for('index'))

@app.route('/profile/<username>', methods=['GET'])
def profile(username):
    if 'username' in session:
        user = users_collection.find_one({'username': username})
        if session['role'] == 'admin' or session['username'] == username:
            return render_template('profile/profile.html', user=user)
        else:
            return "Access denied"
    return redirect(url_for('login'))

@app.route('/edit_profile/<username>', methods=['GET', 'POST'])
def edit_profile(username):
    if 'username' in session and session['username'] == username:
        user = users_collection.find_one({'username': username})
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            if 'username' in request.form:
                new_username = request.form['username']
            else:
                new_username = username

            password = request.form['password']

            updated_data = {
                'name': name,
                'email': email,
                'username': new_username,
            }
            if password:
                hashed_password = generate_password_hash(password)
                updated_data['password'] = hashed_password

            users_collection.update_one({'username': username}, {'$set': updated_data})
            session['username'] = new_username
            return redirect(url_for('profile', username=new_username))

        return render_template('profile/edit_profile.html', user=user)
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    session.clear()
    flash('Anda telah logout', 'success')
    return redirect(url_for('index'))

@app.route('/mahasiswa', methods=['GET', 'POST'])
def mahasiswa():
    if 'username' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return "Access denied"
    
    if request.method == 'POST':
        nim = request.form['nim']
        nama = request.form['nama']
        alamat = request.form['alamat']
        jenis_kelamin = request.form['jenis_kelamin']
        jurusan = request.form.get('jurusan')
        kompetensi = request.form.getlist('kompetensi')
        data = {
            'nim': nim,
            'nama': nama,
            'alamat': alamat,
            'jenis_kelamin': jenis_kelamin,
            'jurusan': jurusan,
            'kompetensi': kompetensi
        }
        mahasiswa_collection.insert_one(data)
        return redirect('/list_mahasiswa')
    
    jurusan = list(jurusan_collection.find())
    kompetensi = list(kompetensi_collection.find())
    return render_template('mahasiswa/mahasiswa.html', jurusan=jurusan, kompetensi=kompetensi)

@app.route('/list_mahasiswa', methods=['GET', 'POST']) 
def get_list_mahasiswa(): 
    if 'username' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return "Access denied"
    
    if request.method == 'POST':
        search_query = request.form['search']
        list_data_mhs = mahasiswa_collection.find({
            '$or': [
                {'nim': {'$regex': search_query, '$options': 'i'}},
                {'nama': {'$regex': search_query, '$options': 'i'}}
            ]
        })
    else:
        list_data_mhs = mahasiswa_collection.find()
    return render_template("mahasiswa/list_mahasiswa.html", data_mahasiswa=list_data_mhs) 

@app.route('/edit/<id>')
def edit_mahasiswa(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return "Access denied"
    
    mahasiswa = mahasiswa_collection.find_one({'_id': ObjectId(id)}) 
    jurusan = jurusan_collection.find()
    kompetensi = kompetensi_collection.find()
    return render_template('mahasiswa/edit_mahasiswa.html', mahasiswa=mahasiswa, jurusan=jurusan, kompetensi=kompetensi)

@app.route('/update/<id>', methods=['POST']) 
def update_mahasiswa(id):
    if 'username' not in session:
        return redirect(url_for('login'))
   
    elif session['role'] != 'admin':
        return "Access denied"
    
    mahasiswa = {
        'nim': request.form['nim'],
        'nama': request.form['nama'],
        'alamat': request.form['alamat'],
        'jenis_kelamin': request.form['jenis_kelamin'],
        'jurusan': request.form.get('jurusan'),
        'kompetensi': request.form.getlist('kompetensi')
    }
    mahasiswa_collection.update_one({'_id': ObjectId(id)}, {'$set': mahasiswa})
    flash('Data mahasiswa berhasil diperbarui', 'success')
    return redirect(url_for('get_list_mahasiswa'))

@app.route('/delete/<id>') 
def delete_mahasiswa(id): 
    if 'username' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return "Access denied"
    
    mahasiswa_collection.delete_one({'_id': ObjectId(id)})
    flash('Data mahasiswa berhasil dihapus', 'success')
    return redirect(url_for('get_list_mahasiswa'))

@app.route('/jurusan', methods=['GET', 'POST']) 
def jurusan():
    if 'username' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return "Access denied"
    
    if request.method == 'POST':
        nama_jurusan = request.form['nama_jurusan']
        data = {
            'nama_jurusan': nama_jurusan
        }
        jurusan_collection.insert_one(data)
        return redirect('/list_jurusan')
    return render_template('jurusan/jurusan.html')

@app.route('/list_jurusan', methods=['GET', 'POST']) 
def get_list_jurusan(): 
    if 'username' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return "Access denied"
    
    list_data_jurusan = jurusan_collection.find()
    return render_template("jurusan/list_jurusan.html", data_jurusan=list_data_jurusan) 

@app.route('/edit_jurusan/<id>')
def edit_jurusan(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return "Access denied"
    
    jurusan = jurusan_collection.find_one({'_id': ObjectId(id)}) 
    return render_template('jurusan/edit_jurusan.html', jurusan=jurusan)

@app.route('/update_jurusan/<id>', methods=['POST']) 
def update_jurusan(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return "Access denied"
    
    jurusan = {
        'nama_jurusan': request.form['nama_jurusan']
    }
    jurusan_collection.update_one({'_id': ObjectId(id)}, {'$set': jurusan})
    flash('Data jurusan berhasil diperbarui', 'success')
    return redirect(url_for('get_list_jurusan'))

@app.route('/delete_jurusan/<id>') 
def delete_jurusan(id): 
    if 'username' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return "Access denied"
    
    jurusan_collection.delete_one({'_id': ObjectId(id)})
    flash('Data jurusan berhasil dihapus', 'success')
    return redirect(url_for('get_list_jurusan'))

@app.route('/kompetensi', methods=['GET', 'POST']) 
def kompetensi():
    if 'username' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return "Access denied"
    
    if request.method == 'POST':
        nama_kompetensi = request.form['nama_kompetensi']
        data = {
            'nama_kompetensi': nama_kompetensi
        }
        kompetensi_collection.insert_one(data)
        return redirect('/list_kompetensi')
    return render_template('kompetensi/kompetensi.html')

# Fungsi get_list_kompetensi
@app.route('/list_kompetensi', methods=['GET', 'POST']) 
def get_list_kompetensi(): 
    if 'username' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return "Access denied"
    
    list_data_kompetensi = kompetensi_collection.find()
    return render_template("kompetensi/list_kompetensi.html", data_kompetensi=list_data_kompetensi) 


@app.route('/edit_kompetensi/<id>')
def edit_kompetensi(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return "Access denied"
    
    kompetensi = kompetensi_collection.find_one({'_id': ObjectId(id)}) 
    return render_template('kompetensi/edit_kompetensi.html', kompetensi=kompetensi)

@app.route('/update_kompetensi/<id>', methods=['POST']) 
def update_kompetensi(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return "Access denied"
    
    kompetensi = {
        'nama_kompetensi': request.form['nama_kompetensi']
    }
    kompetensi_collection.update_one({'_id': ObjectId(id)}, {'$set': kompetensi})
    flash('Data kompetensi berhasil diperbarui', 'success')
    return redirect(url_for('get_list_kompetensi'))

@app.route('/delete_kompetensi/<id>') 
def delete_kompetensi(id): 
    if 'username' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return "Access denied"
    
    kompetensi_collection.delete_one({'_id': ObjectId(id)})
    flash('Data kompetensi berhasil dihapus', 'success')
    return redirect(url_for('get_list_kompetensi'))

@app.route('/dosen')
def dosen_form():
    if 'username' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return "Access denied"
    
    return render_template('dosen/dosen.html')

@app.route('/dosen', methods=['POST'])
def add_dosen():
    if 'username' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return "Access denied"
    
    if request.method == 'POST':
        nama_dosen = request.form['nama_dosen']
        nip = request.form['nip']
        alamat = request.form['alamat']
        jenis_kelamin = request.form['jenis_kelamin']
        
        data = {
            'nama_dosen': nama_dosen,
            'nip': nip,
            'alamat': alamat,
            'jenis_kelamin': jenis_kelamin
        }
        dosen_collection.insert_one(data)
        return redirect('/list_dosen')

@app.route('/list_dosen')
def list_dosen():
    if 'username' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return "Access denied"
    
    list_data_dosen = dosen_collection.find()
    return render_template("dosen/list_dosen.html", data_dosen=list_data_dosen)

@app.route('/edit_dosen/<id>')
def edit_dosen(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return "Access denied"
    
    dosen = dosen_collection.find_one({'_id': ObjectId(id)})
    return render_template('dosen/edit_dosen.html', dosen=dosen)

@app.route('/update_dosen/<id>', methods=['POST'])
def update_dosen(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return "Access denied"
    
    if request.method == 'POST':
        dosen = {
            'nama_dosen': request.form['nama_dosen'],
            'nip': request.form['nip'],
            'alamat': request.form['alamat'],
            'jenis_kelamin': request.form['jenis_kelamin']
        }
        dosen_collection.update_one({'_id': ObjectId(id)}, {'$set': dosen})
        flash('Data dosen berhasil diperbarui', 'success')
        return redirect(url_for('list_dosen'))

@app.route('/delete_dosen/<id>')
def delete_dosen(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return "Access denied"
    
    dosen_collection.delete_one({'_id': ObjectId(id)})
    flash('Data dosen berhasil dihapus', 'success')
    return redirect(url_for('list_dosen'))

@app.route('/konsultasi', methods=['GET', 'POST'])
def konsultasi():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        nama = request.form['nama']
        dosen = request.form.get('dosen')
        waktu = request.form['waktu']
        laporan = request.form['laporan']

        data_konsultasi = {
            'nama': nama,
            'dosen': dosen,
            'waktu': waktu,
            'laporan': laporan,
            'user_id': session['user_id']
        }

        konsultasi_collection.insert_one(data_konsultasi)
        flash('Konsultasi berhasil ditambahkan', 'success')
        return redirect(url_for('get_list_konsultasi'))

    data_dosen = list(dosen_collection.find())
    return render_template('konsultasi/konsultasi.html', data_dosen=data_dosen)

@app.route('/list_konsultasi', methods=['GET', 'POST'])
def get_list_konsultasi():
    if 'username' not in session:
        return redirect(url_for('login'))

    if session['role'] == 'admin':
        if request.method == 'POST':
            search_query = request.form['search']
            list_data_ksl = konsultasi_collection.find({
                '$or': [
                    {'nama': {'$regex': search_query, '$options': 'i'}},
                    {'dosen': {'$regex': search_query, '$options': 'i'}}
                ]
            })
        else:
            list_data_ksl = konsultasi_collection.find()
    else:
        if request.method == 'POST':
            search_query = request.form['search']
            list_data_ksl = konsultasi_collection.find({
                '$and': [
                    {'user_id': session['user_id']},
                    {'$or': [
                        {'waktu': {'$regex': search_query, '$options': 'i'}},
                        {'dosen': {'$regex': search_query, '$options': 'i'}}
                    ]}
                ]
            })
        else:
            list_data_ksl = konsultasi_collection.find({'user_id': session['user_id']})
    
    return render_template('konsultasi/list_konsultasi.html', data_konsultasi=list_data_ksl)

@app.route('/delete_konsultasi/<id>')
def delete_konsultasi(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    db.konsultasi.delete_one({'_id': ObjectId(id)})

    flash('Konsultasi berhasil dihapus', 'success')
    return redirect(url_for('get_list_konsultasi'))

@app.route('/admin', methods=['GET', 'POST'])
def admin_registration():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        existing_user = users_collection.find_one({'username': username})
        if existing_user:
            flash('Username already exists! Please choose another one.', 'danger')
            return redirect(url_for('admin_registration'))
        hashed_password = generate_password_hash(password)
        user_data = {
            'name': name,
            'email': email,
            'username': username,
            'password': hashed_password,
            'role': 'admin'
        }
        users_collection.insert_one(user_data)
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True)