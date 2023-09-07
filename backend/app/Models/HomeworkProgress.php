<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class HomeworkProgress extends Model
{
    protected $table = 'homework_progress';
    /**
     * The attributes that are mass assignable.
     *
     * @var array<int, string>
     */
    protected $fillable = [
        'user_id', 'homework_id', 'progress', 'notes', 'link'
    ];

    public function user(){
        return $this->belongsTo(User::class);
    }

    public function homework(){
        return $this->belongsTo(Homework::class);
    }

    /**
     * The attributes that should be hidden for serialization.
     *
     * @var array<int, string>
     */
    protected $hidden = [
    ];

    /**
     * The attributes that should be cast.
     *
     * @var array<string, string>
     */
    protected $casts = [
    ];
}