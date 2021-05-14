"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from gamerraterapi.models import Review, Game, Player

class ReviewView(ViewSet):

    def create(self, request):
        
        player = Player.objects.get(user=request.auth.user)

        
        review = Review()
        review.review = request.data["review"]
        review.rating = request.data["rating"]

        game = Game.objects.get(pk=request.data["gameId"])
        review.game = game

        player = Player.objects.get(pk=request.data["playerId"])
        review.player = player

        try:
            review.save()

            serializer = ReviewSerializer(review, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk=None):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game instance
        """
        try:
            
            review = Review.objects.get(pk=pk)
            serializer = ReviewSerializer(review, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """
        player = Player.objects.get(user=request.auth.user)
        
        review = Review()
        review.review = request.data["review"]
        review.rating = request.data["rating"]

        game = Game.objects.get(pk=request.data["gameId"])
        review.game = game

        player = Player.objects.get(pk=request.data["playerId"])
        review.player = player

        game.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single game

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            review = Review.objects.get(pk=pk)
            review.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Review.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to games resource

        Returns:
            Response -- JSON serialized list of games
        """
        
        reviews = Review.objects.all()

        serializer = ReviewSerializer(
            reviews, many=True, context={'request': request})

        return Response(serializer.data)

class ReviewSerializer(serializers.ModelSerializer):
    """JSON serializer for categories

    Arguments:
        serializer type
    """
    class Meta:
        model = Review
        fields = ('id', 'review', 'rating', 'game', 'player')
        depth = 1

