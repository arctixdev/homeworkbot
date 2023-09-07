<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use App\Models\HomeworkProgress;

class User extends Model
{
    /**
     * The attributes that are mass assignable.
     *
     * @var array<int, string>
     */
    protected $fillable = [
        'username', 'nickname', 'discord_id'
    ];

    public function homeworks(){
        return $this->hasMany(HomeworkProgress::class);
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
