<?php declare(strict_types=1);

namespace App\GraphQL\Mutations;

use App\Models\User;
use App\Models\Homework;
use App\Models\HomeworkProgress;

final readonly class CreateHomework
{
    /** @param  array{}  $args */
    public function __invoke(null $_, array $args)
    {
        $homework = new Homework(['name' => $args['name'], 'link' => $args['link'], 'subject' => $args['subject'], 'description' => $args['description'], 'date_due' => $args['date_due']]);
        $homework->save();
        foreach (User::all() as $user) {
            $homework_progress = new HomeworkProgress(['user_id' => $user->id, 'homework_id' => $homework->id, 'progress' => 0, 'notes' => '', 'link' => '']);
            $homework_progress->save();
        }
        return $homework;
    }
}
